import os
from openai import OpenAI

from model_client import get_client


def extract_json(payload, config=None):
    client = get_client(config)
    response = client.chat.completions.create(model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': 'Extract the following text into structured JSON:

' + payload['text']}])
    return {'json': response.choices[0].message.content or ''}