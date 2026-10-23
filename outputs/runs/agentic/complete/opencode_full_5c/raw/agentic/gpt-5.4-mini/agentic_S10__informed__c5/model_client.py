import os
from functools import lru_cache

from openai import OpenAI


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def pick_model(preferred=None, family=None):
    if preferred:
        return preferred
    if family == "embedding":
        return DEFAULT_EMBEDDING_MODEL
    return DEFAULT_CHAT_MODEL


def ensure_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)
