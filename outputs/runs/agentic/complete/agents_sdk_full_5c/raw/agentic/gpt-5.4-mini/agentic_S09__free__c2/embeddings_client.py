import os
from functools import lru_cache

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    base_url = os.getenv(OPENAI_BASE_URL_ENV)
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def get_embedding_model(default: str = "text-embedding-3-small") -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", default)
