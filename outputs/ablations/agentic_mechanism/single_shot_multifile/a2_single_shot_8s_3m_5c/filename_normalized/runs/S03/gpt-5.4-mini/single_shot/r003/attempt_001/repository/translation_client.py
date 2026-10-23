import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key) if api_key else OpenAI()


def get_translation_model(default: str) -> str:
    return os.getenv("OPENAI_TRANSLATION_MODEL", default)
