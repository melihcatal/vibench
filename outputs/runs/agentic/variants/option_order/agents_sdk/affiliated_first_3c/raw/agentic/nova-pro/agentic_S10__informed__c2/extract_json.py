from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(api_key='MISTRAL_API_KEY')

def extract_json(text):
    messages = [ChatMessage(role='user', content=text)]
    chat_response = client.chat(model='mistral-medium', messages=messages)
    return chat_response.choices[0].message.content