import os
from [HELPER] model_client import ModelClient

client = ModelClient()

def summarize_text(text):
    response = client.call_model('text-davinci-003', {'prompt': text,'max_tokens': 150})
    return response['choices'][0]['text'].strip()
