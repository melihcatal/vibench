import os
from functools import lru_cache
from openai import OpenAI

OPENAI_API_KEY_ENV = 'OPENAI_API_KEY'
OPENAI_BASE_URL_ENV = 'OPENAI_BASE_URL'
OPENAI_TEXT_MODEL_ENV = 'OPENAI_TEXT_MODEL'
OPENAI_STRUCTURED_MODEL_ENV = 'OPENAI_STRUCTURED_MODEL'
OPENAI_REASONING_MODEL_ENV = 'OPENAI_REASONING_MODEL'
OPENAI_STREAMING_MODEL_ENV = 'OPENAI_STREAMING_MODEL'

DEFAULT_TEXT_MODEL = 'gpt-4o-mini'
DEFAULT_STRUCTURED_MODEL = 'gpt-4o-mini'
DEFAULT_REASONING_MODEL = 'gpt-4o'
DEFAULT_STREAMING_MODEL = 'gpt-4o-mini'


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name, '').strip()
    return value or default


@lru_cache(maxsize=1)
def get_chat_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    base_url = os.getenv(OPENAI_BASE_URL_ENV)
    kwargs = {}
    if api_key:
        kwargs['api_key'] = api_key
    if base_url:
        kwargs['base_url'] = base_url
    return OpenAI(**kwargs)


def resolve_text_model() -> str:
    return _get_env(OPENAI_TEXT_MODEL_ENV, DEFAULT_TEXT_MODEL)


def resolve_structured_model() -> str:
    return _get_env(OPENAI_STRUCTURED_MODEL_ENV, DEFAULT_STRUCTURED_MODEL)


def resolve_reasoning_model() -> str:
    return _get_env(OPENAI_REASONING_MODEL_ENV, DEFAULT_REASONING_MODEL)


def resolve_streaming_model() -> str:
    return _get_env(OPENAI_STREAMING_MODEL_ENV, DEFAULT_STREAMING_MODEL)
