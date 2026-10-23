import os
from openai import OpenAI


def get_client(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ['OPENAI_API_KEY']
    return OpenAI(api_key=api_key)


def get_model(model_name='gpt-5.4-mini'):
    return model_name