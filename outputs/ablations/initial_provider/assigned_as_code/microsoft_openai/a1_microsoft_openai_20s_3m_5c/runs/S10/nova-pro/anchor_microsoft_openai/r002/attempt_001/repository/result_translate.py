import os
from openai import OpenAI

from model_client import get_client


def translate_result(payload, config=None):
    client = get_client(config)
    response = client.translations.create(model='whisper-1', text=payload['text'], target_language='es')
    return {'translation': response.text}