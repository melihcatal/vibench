import os
from openai import OpenAI


DEFAULT_MODEL = 'gpt-5.4-mini'


def get_config(config=None):
    config = config or {}
    return {
        'api_key': config.get('api_key') or os.environ.get('OPENAI_API_KEY'),
        'model': config.get('model') or os.environ.get('OPENAI_MODEL', DEFAULT_MODEL),
    }


def get_client(config=None):
    resolved = get_config(config)
    return OpenAI(api_key=resolved['api_key'])


def get_model(config=None):
    return get_config(config)['model']
