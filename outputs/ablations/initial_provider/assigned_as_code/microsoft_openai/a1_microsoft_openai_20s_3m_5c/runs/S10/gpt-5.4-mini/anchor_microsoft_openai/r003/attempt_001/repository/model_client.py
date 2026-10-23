import os
from openai import OpenAI


DEFAULT_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-5.4-mini')


def get_client(config=None):
    config = config or {}
    return OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])


def get_model(config=None):
    config = config or {}
    return config.get('model') or os.environ.get('OPENAI_MODEL') or DEFAULT_MODEL


def build_messages(system_prompt, user_content):
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_content})
    return messages
