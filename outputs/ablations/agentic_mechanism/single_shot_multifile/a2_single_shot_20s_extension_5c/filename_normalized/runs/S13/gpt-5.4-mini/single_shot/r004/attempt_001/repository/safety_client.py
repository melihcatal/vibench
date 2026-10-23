import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL_ENV = "OPENAI_MODERATION_MODEL"
DEFAULT_OPENAI_MODERATION_MODEL = "gpt-4.1-mini"


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return OpenAI(api_key=api_key)


def moderation_model_name() -> str:
    return os.getenv(OPENAI_MODERATION_MODEL_ENV, DEFAULT_OPENAI_MODERATION_MODEL)
