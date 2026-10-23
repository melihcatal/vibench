import os
from functools import lru_cache
from openai import OpenAI


def get_platform_model_id() -> str:
    return os.getenv("OPENAI_PLATFORM_MODEL_ID", "gpt-4.1-mini")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_platform_client() -> OpenAI:
    return get_openai_client()
