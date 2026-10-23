import os
from [HELPER] model_client import ModelClient

client = ModelClient()

def extract_json(text):
    response = client.call_model('text-davinci-003', {'prompt': text,'max_tokens': 200})
    return response['choices'][0]['text'].strip()
