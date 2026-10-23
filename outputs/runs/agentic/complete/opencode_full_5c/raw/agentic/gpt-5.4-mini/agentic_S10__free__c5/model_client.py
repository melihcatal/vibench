import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_model_family() -> str:
    return os.environ.get("OPENAI_MODEL_FAMILY", "gpt-5.4-mini")


def get_text_model() -> str:
    return os.environ.get("OPENAI_TEXT_MODEL", "openai/gpt-5.4-mini")


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
