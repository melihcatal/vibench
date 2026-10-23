import os
from typing import Any, Dict

from openai import OpenAI


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def translation_model_name() -> str:
    return os.environ.get("TRANSLATION_MODEL", "gpt-5.4-mini")


def build_translation_messages(
    source_language: str, target_language: str, text: str
) -> list[Dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": f"Translate from {source_language} to {target_language} while preserving meaning.",
        },
        {"role": "user", "content": text},
    ]


def chat_completion(
    client: OpenAI, messages: list[Dict[str, Any]], temperature: float = 0.2
) -> str:
    response = client.chat.completions.create(
        model=translation_model_name(), messages=messages, temperature=temperature
    )
    return response.choices[0].message.content or ""
