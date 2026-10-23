import os
from mistralai.client import MistralClient

mistral_api_key = os.getenv('MISTRAL_API_KEY')

def summarize_onboarding(text):
    client = MistralClient(api_key=mistral_api_key)
    summary = client.chat(model='mistral-medium', messages=[{'role': 'user', 'content': text}])
    return summary.choices[0].message.content