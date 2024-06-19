import requests
import json
message = 'I love carbs myself -- bread is tasty.'
history = []
json_doc = json.dumps({ 'user_input' : message, "history": []})
result = requests.post('http://localhost:8888/', json = json_doc).json()
print(result)
history += [message, result["response"]]
json_doc = json.dumps({ 'user_input' : message, 'history' : history })
result = requests.post('http://localhost:8888/', json = json_doc).json()
print(result)
