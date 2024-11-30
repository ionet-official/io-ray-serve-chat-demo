import torch
from typing import Dict

from ray.serve import Application
from ray import serve
from starlette.requests import Request
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


@serve.deployment(ray_actor_options={"num_gpus": 0.5})
class Chat:
    def __init__(self, model: str):
        # configure stateful elements of our service such as loading a model
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        print(f"Loading model: {model}")
        self._model = AutoModelForSeq2SeqLM.from_pretrained(model, torch_dtype=torch.float16).to(0)
        self._max_length = self._model.config.max_position_embeddings
        print(f"Model loaded. Max length for the model: {self._max_length}")

    async def __call__(self, request: Request) -> Dict:
        # path to handle HTTP requests
        data = await request.json()

        # after decoding the payload, we delegate to get_response for logic
        return {"response": self.get_response(data["user_input"], data["history"])}

    def get_response(self, user_input: str, history: list[str]) -> str:
        # this method receives calls directly (from Python) or from __call__ (from HTTP)
        # the history is client-side state and will be a list of raw strings
        # older pair of messages from history is used as long as it fits the model's max length

        # Trim the history until total input fits max_lenght
        while True:
            input_text = "\n".join(history + [user_input])
            if len(history) == 0 or len(self._tokenizer.encode(input_text)) <= self._max_length:
                break
            history = history[2:]

        inputs = self._tokenizer([input_text], max_length=self._max_length, truncation=True, return_tensors="pt").to(0)
        reply_ids = self._model.generate(**inputs, max_length=self._max_length)
        response = self._tokenizer.batch_decode(reply_ids, skip_special_tokens=True)
        return response[0].strip()


def app_builder(args: Dict[str, str]) -> Application:
    return Chat.bind(model="facebook/blenderbot-400M-distill")


app = app_builder(None)
