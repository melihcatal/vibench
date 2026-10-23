import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(document_text: str, schema: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
    system = (
        "You extract structured fields from OCR-normalized document text. "
        "Return only valid JSON. "
        "If a field is missing, use null. "
        "Prefer exact values found in the text."
    )
    if schema is not None:
        system += f" Use this target schema: {json.dumps(schema, ensure_ascii=False)}"
    user = f"Document text:\n{document_text}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def extract_fields(document_text: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(document_text, schema),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return json.loads(content)


def extract_fields_from_text(document_text: str) -> Dict[str, Any]:
    return extract_fields(document_text)
