import os
from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = 'text-embedding-3-small'


def load_config(config=None):
    config = config or {}
    return {
        'api_key': config.get('api_key') or os.environ.get('OPENAI_API_KEY'),
        'model': config.get('model') or DEFAULT_EMBEDDING_MODEL,
    }


def get_client(config=None):
    cfg = load_config(config)
    return OpenAI(api_key=cfg['api_key']), cfg
