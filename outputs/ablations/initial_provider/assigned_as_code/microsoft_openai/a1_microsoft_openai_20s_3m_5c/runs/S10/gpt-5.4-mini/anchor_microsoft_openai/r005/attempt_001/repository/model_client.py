import os
from openai import OpenAI


DEFAULT_MODEL = 'gpt-5.4-mini'


def get_api_key(config=None):
    config = config or {}
    return config.get('api_key') or os.environ['OPENAI_API_KEY']


def get_model(config=None):
    config = config or {}
    return config.get('model') or DEFAULT_MODEL


def get_client(config=None):
    return OpenAI(api_key=get_api_key(config))


def chat_completion(messages, config=None, **kwargs):
    client = get_client(config)
    return client.chat.completions.create(model=get_model(config), messages=messages, **kwargs)


def embed_texts(texts, config=None, **kwargs):
    client = get_client(config)
    model = (config or {}).get('embedding_model') or 'text-embedding-3-small'
    return client.embeddings.create(model=model, input=texts, **kwargs)
