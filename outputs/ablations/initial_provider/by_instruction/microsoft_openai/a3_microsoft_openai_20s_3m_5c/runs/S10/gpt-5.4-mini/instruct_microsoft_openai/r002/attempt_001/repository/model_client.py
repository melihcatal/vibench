import os
from typing import Any, Dict

from openai import OpenAI


def provider_name() -> str:
    return "openai"


def default_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))


def normalize_messages(text: str, system: str | None = None) -> list[Dict[str, str]]:
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": text})
    return msgs


def response_text(response: Any) -> str:
    return response.output_text if hasattr(response, "output_text") else str(response)
