from __future__ import annotations

import json
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import JsonExtractionResult


_PROVIDER = "openai"
_DEFAULT_EXTRACT_MODEL = "gpt-4o-mini"


def extract_json(text: str, schema_hint: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> JsonExtractionResult:
    """Extract structured JSON from text using OpenAI Chat Completions."""
    model_name = model or get_model_name("extract_json", _DEFAULT_EXTRACT_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="You extract structured data and return valid JSON only.",
        user=f"Extract data as JSON matching this schema hint:\n{schema_hint}\n\nText:\n{text}",
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0,
    )
    content = response.choices[0].message.content or "{}"
    payload: Dict[str, Any] = json.loads(content)
    return JsonExtractionResult(provider=_PROVIDER, model=model_name, data=payload)
