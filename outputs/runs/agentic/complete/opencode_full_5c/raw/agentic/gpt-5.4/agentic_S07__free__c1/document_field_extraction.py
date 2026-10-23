from __future__ import annotations

import os
from typing import Any, Dict

import requests


def extract_document_fields(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: OPENAI_API_KEY")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4.1-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": "Extract structured document fields from OCR text and return only JSON that matches the requested schema.",
                },
                {
                    "role": "user",
                    "content": {"schema": schema, "document_text": text},
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": "gpt-4.1-mini", "content": content}
