import os
from [HELPER] model_client import ModelClient

client = ModelClient()

def stream_completion(prompt):
    for response in client.stream_model('text-davinci-003', {'prompt': prompt,'max_tokens': 100}):
        yield response['choices'][0]['text'].strip()
