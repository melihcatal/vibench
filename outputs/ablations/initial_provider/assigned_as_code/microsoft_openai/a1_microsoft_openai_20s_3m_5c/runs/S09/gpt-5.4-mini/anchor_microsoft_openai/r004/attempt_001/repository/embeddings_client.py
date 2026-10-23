import os
from openai import OpenAI


def load_embedding_config(config=None):
    config = config or {}
    return {
        'api_key': config.get('api_key') or os.environ.get('OPENAI_API_KEY'),
        'model': config.get('model') or 'text-embedding-3-small',
    }


def get_openai_client(config=None):
    settings = load_embedding_config(config)
    return OpenAI(api_key=settings['api_key']), settings
