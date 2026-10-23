import os
from openai import OpenAI


def get_client(config=None):
    config = config or {}
    return OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])