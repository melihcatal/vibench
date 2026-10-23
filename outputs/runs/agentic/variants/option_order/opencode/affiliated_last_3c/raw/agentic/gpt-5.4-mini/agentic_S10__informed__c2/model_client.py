import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model_family(default: str = "gpt-4.1-mini") -> str:
    return os.getenv("MODEL_FAMILY", default)


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()
