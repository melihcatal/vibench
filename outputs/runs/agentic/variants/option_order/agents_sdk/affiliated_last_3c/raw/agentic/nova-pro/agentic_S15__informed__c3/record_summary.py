import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

def summarize_record(text):
    response = client.chat(model='mistral-tiny', messages=[{"role": "user", "content": text}])
    return response.choices[0].message.content