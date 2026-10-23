import os
from typing import Any, Dict, Optional

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_DOC_EXTRACTION_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def build_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def request_chat_json(system_prompt: str, user_payload: Dict[str, Any], *, model: str = OPENAI_MODEL) -> Dict[str, Any]:
    client = build_openai_client()
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(user_payload)},
        ],
        text={"format": {"type": "json_object"}},
    )
    return response.output_text and __import__("json").loads(response.output_text) or {}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
