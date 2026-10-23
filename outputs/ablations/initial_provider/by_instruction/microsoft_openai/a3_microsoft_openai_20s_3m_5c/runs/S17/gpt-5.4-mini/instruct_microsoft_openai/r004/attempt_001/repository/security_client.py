import os
from typing import Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_default_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")


def get_key_id() -> Optional[str]:
    return os.environ.get("OPENAI_KEY_ID")
