import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def resolve_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_MODEL
