import os
from functools import lru_cache

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def choose_chat_model(preferred: str | None = None) -> str:
    return preferred or DEFAULT_MODEL


def choose_embedding_model(preferred: str | None = None) -> str:
    return preferred or DEFAULT_EMBEDDING_MODEL


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()
