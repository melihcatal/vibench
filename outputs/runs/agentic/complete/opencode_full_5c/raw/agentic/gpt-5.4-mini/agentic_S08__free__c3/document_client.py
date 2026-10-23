import os
from typing import Any, Dict

from openai import OpenAI


def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


def get_client() -> OpenAI:
    return OpenAI(api_key=get_api_key() or None)


def get_model() -> str:
    return os.getenv("OPENAI_DOCUMENT_MODEL", "gpt-4.1-mini")


def normalize_text_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"text": str(payload)}
