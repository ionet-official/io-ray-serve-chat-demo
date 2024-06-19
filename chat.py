import ray
import requests, json
from starlette.requests import Request
from typing import Dict
from ray.serve import Application
from ray import serve
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
@serve.deployment(ray_actor_options={'num_gpus': 0.5})
class Chat:
    def __init__(self, model: str):
        # configure stateful elements of our service such as loading a model
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        self._model =  AutoModelForSeq2SeqLM.from_pretrained(model).to(0)

    async def __call__(self, request: Request) -> Dict:
        # path to handle HTTP requests
        data = await request.json()
        data = json.loads(data)
        # after decoding the payload, we delegate to get_response for logic
        return {'response': self.get_response(data['user_input'], data['history']) }

    def get_response(self, user_input: str, history: list[str]) -> str:
        # this method receives calls directly (from Python) or from __call__ (from HTTP)
        # the history is client-side state and will be a list of raw strings;
        # for the default config of the model and tokenizer, history should be joined with '</s><s>'
        inputs = self._tokenizer('</s><s>'.join(user_input), return_tensors='pt').to(0)
        print(inputs)
        reply_ids = self._model.generate(**inputs, max_new_tokens=500)
        print(reply_ids)
        response = self._tokenizer.batch_decode(reply_ids.cpu(), skip_special_tokens=True)
        print(response)
        return response[0]

def app_builder(args: Dict[str, str])->Application:
    return Chat.bind(model='facebook/blenderbot-400M-distill')

app = app_builder(None)
