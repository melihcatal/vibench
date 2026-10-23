import json
import os
from typing import Any, Dict, Optional

import httpx


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(text: str, schema_hint: Optional[str] = None) -> list[dict[str, str]]:
    system = "Extract structured JSON from the provided text. Return only valid JSON."
    if schema_hint:
        system += f" Follow this schema hint: {schema_hint}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]


def extract_json(text: str, schema_hint: Optional[str] = None, timeout: float = 60.0) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": _build_messages(text, schema_hint),
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=timeout) as client:
        response = client.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        return json.loads(content)
    return content
