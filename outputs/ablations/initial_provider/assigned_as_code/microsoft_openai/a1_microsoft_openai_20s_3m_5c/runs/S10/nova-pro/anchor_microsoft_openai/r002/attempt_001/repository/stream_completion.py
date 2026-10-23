import os
from openai import OpenAI

from model_client import get_client


def stream_completion(payload, config=None):
    client = get_client(config)
    response = client.chat.completions.create(model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': payload['text']}], stream=True)
    for chunk in response:
        yield chunk.choices[0].delta.content or ''