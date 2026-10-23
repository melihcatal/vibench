import os
from functools import lru_cache

from openai import OpenAI


def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=get_api_key() or None)


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def get_key_reference() -> str:
    return os.getenv("OPENAI_KEY_REFERENCE", "managed-key")
