import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

def summarize_text(text):
    messages = [ChatMessage(role='user', content=text)]
    chat_response = client.chat(model='mistral-large', messages=messages)
    return chat_response.choices[0].message.content