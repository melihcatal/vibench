import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translation_model() -> str:
    return os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_prompt(source_language: str, target_language: str, text: str) -> str:
    return f"Translate from {source_language} to {target_language}. Preserve meaning and formatting. Text: {text}"
