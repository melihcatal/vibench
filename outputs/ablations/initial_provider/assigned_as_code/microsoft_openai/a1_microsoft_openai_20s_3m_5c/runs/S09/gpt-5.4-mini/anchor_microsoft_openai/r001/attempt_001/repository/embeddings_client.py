import os
from openai import OpenAI


def get_api_key(config=None):
    config = config or {}
    return config.get('api_key') or os.environ['OPENAI_API_KEY']


def get_client(config=None):
    return OpenAI(api_key=get_api_key(config))


def get_embedding_model(config=None):
    config = config or {}
    return config.get('model') or 'text-embedding-3-small'
