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
