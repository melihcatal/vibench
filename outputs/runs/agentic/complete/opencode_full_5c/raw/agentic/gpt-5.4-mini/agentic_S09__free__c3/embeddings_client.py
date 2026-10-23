import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=api_key())


def embedding_model() -> str:
    return DEFAULT_EMBEDDING_MODEL
