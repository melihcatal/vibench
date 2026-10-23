import os
from functools import lru_cache

from openai import OpenAI


def get_model_name(default: str = "gpt-4o-mini") -> str:
    return os.getenv("OPENAI_MODEL", default)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()
