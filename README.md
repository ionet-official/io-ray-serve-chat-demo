# io-ray-serve-chat-demo
a Ray Serve Chat Demo Serving Hugging Face Models


# How to get started 

1. Open Up Io.net Account
2. Follow through standard procedure on launching a Ray Cluster. Select a small cluster, for example 4 T4.
3. When the cluster is ready, select Visual Studio Code
4. Launch Visual studio code terminal and clone this repo `git clone https://github.com/ionet-official/io-ray-serve-chat-demo.git`
5. Go to the folder `cd  io-ray-serve-chat-demo`
6. Start the chat server via `ray serve run chat.yaml`
7. Wait till the Ray serve deploys the chat app across workers.
8. Remember the current vscode url. It looks like this  `https://vscode-1d47a.tunnels.io.systems/`
9. Replace the `vscode` section with `exposed-service`, you will obtain the Chat server serve endpoint
10. You can use below code snippet to interact with the Ray serve application created
```
import requests
import json
message = 'I love carbs myself -- bread is tasty.'
history = []
json_doc = json.dumps({ 'user_input' : message, "history": []})
result = requests.post('https://exposed-service-1d47a.tunnels.io.systems/', json = json_doc).json()
print(result)
```
