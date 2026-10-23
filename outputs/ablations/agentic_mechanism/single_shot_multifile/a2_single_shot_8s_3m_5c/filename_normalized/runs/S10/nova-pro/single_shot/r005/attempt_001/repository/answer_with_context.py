import os
from [HELPER] model_client import ModelClient

client = ModelClient()

def answer_with_context(question, context):
    prompt = f'Context: {context}\nQuestion: {question}\nAnswer:'
    response = client.call_model('text-davinci-003', {'prompt': prompt,'max_tokens': 100})
    return response['choices'][0]['text'].strip()
