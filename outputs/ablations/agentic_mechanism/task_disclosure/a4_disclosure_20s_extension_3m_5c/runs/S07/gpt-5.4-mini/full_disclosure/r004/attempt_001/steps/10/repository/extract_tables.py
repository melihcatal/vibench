import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_TABLE_MODEL = os.getenv("OPENAI_TABLE_MODEL", "gpt-4o-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def _document_to_data_url(document_bytes: bytes, mime_type: str = "application/pdf") -> str:
    encoded = base64.b64encode(document_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def extract_tables_from_document(document_bytes: bytes, mime_type: str = "application/pdf", extra_instructions: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = "Extract table structure from this document. Return a JSON object with tables, rows, and cells preserving cell text, row order, and column spans if present."
    if extra_instructions:
        prompt = f"{prompt} {extra_instructions}"

    payload: Dict[str, Any] = {
        "model": OPENAI_TABLE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": _document_to_data_url(document_bytes, mime_type)}},
                ],
            }
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"tables": [], "raw": content}


def extract_tables_from_file(path: str, mime_type: Optional[str] = None, extra_instructions: Optional[str] = None) -> Dict[str, Any]:
    with open(path, "rb") as f:
        document_bytes = f.read()
    if mime_type is None:
        lower = path.lower()
        if lower.endswith(".png"):
            mime_type = "image/png"
        elif lower.endswith(".jpg") or lower.endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif lower.endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "application/pdf"
    return extract_tables_from_document(document_bytes, mime_type=mime_type, extra_instructions=extra_instructions)
