import os
from openai import OpenAI


def get_openai_api_key(config=None):
    config = config or {}
    return config.get('api_key') or os.environ['OPENAI_API_KEY']


def get_embeddings_model(config=None):
    config = config or {}
    return config.get('model') or 'text-embedding-3-small'


def get_openai_client(config=None):
    return OpenAI(api_key=get_openai_api_key(config))
