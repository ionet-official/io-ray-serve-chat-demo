import requests

SERVER_ENDPOINT = "http://localhost:8778/"

def send_message(message, history):
    try:
        response = requests.post(SERVER_ENDPOINT, json={"user_input": message, "history": history})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


history = []

print("Chatbot session started. If you want to stop the chat, type exit")
print(20 * "-")
while True:
    message = input("You: ")
    if message.lower() == "exit":
        print("Stopping the chat... bye.")
        break

    response = send_message(message, history)
    if response:
        bot_response = response.get("response", "")
        history.extend([f"User: {message}", f"Bot: {bot_response}"])
        print(f"Bot: {bot_response}")
