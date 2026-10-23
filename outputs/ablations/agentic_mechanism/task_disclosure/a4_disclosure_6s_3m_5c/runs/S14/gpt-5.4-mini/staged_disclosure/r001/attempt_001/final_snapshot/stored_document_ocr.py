import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _load_document_payload(stored_document: Any) -> Dict[str, Any]:
    if stored_document is None:
        raise ValueError("stored_document is required")
    if isinstance(stored_document, dict):
        return stored_document
    if isinstance(stored_document, str):
        try:
            return json.loads(stored_document)
        except json.JSONDecodeError as exc:
            raise ValueError("stored_document must be a dict or JSON string") from exc
    raise TypeError("stored_document must be a dict or JSON string")


def _extract_document_source(payload: Dict[str, Any]) -> str:
    for key in ("content_url", "document_url", "file_url", "url"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    for key in ("content_base64", "document_base64", "file_base64", "base64"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return f"data:application/octet-stream;base64,{value}"
    raise ValueError("stored_document must contain a document URL or base64 content")


def run_stored_document_ocr(stored_document: Any, api_key: Optional[str] = None) -> str:
    payload = _load_document_payload(stored_document)
    document_source = _extract_document_source(payload)
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    if document_source.startswith("data:"):
        image_url = document_source
    else:
        image_url = document_source

    request_body = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all readable text from this document. Return only the OCR text."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=request_body,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
