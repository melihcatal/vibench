import os
from functools import lru_cache

from openai import OpenAI


def get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_texts(texts):
    if isinstance(texts, str):
        return [texts]
    return [str(text) for text in texts]
