import os
from functools import lru_cache

from openai import OpenAI


def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=get_api_key())


def get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
