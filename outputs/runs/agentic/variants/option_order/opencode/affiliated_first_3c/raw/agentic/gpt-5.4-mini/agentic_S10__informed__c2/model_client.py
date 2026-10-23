import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-5.4-mini"


def get_model_name() -> str:
    return os.getenv("MODEL_NAME", DEFAULT_MODEL)


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=get_api_key())


def create_messages(system: str, user: str):
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
