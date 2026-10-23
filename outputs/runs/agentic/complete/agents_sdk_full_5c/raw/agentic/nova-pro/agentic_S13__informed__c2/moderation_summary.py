import os
from mistralai.client import MistralClient

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def moderation_summary(text):
    client = MistralClient(api_key=MISTRAL_API_KEY)
    response = client.chat(model='mistral-medium', messages=[{'role': 'user', 'content': text}])
    return response.choices[0].message.content