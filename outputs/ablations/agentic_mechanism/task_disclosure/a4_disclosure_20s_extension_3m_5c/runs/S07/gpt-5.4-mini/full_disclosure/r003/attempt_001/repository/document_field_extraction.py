import os
from typing import Any, Dict, Iterable, List, Optional

import requests

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_FIELD_EXTRACTION_MODEL", "gpt-5.4-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _build_prompt(document_text: str, fields: Optional[Iterable[str]]) -> str:
    field_list = list(fields or [])
    fields_part = ""
    if field_list:
        fields_part = "
Expected fields: " + ", ".join(field_list)
    return (
        "Extract structured fields from the document text. "
        "Return a single JSON object with only the extracted fields and values."
        f"{fields_part}

Document text:
{document_text}"
    )


def extract_structured_fields(document_text: str, fields: Optional[Iterable[str]] = None, *, model: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    if not document_text:
        return {}
    payload = {
        "model": model or OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You extract structured data from OCR-normalized document text."},
            {"role": "user", "content": _build_prompt(document_text, fields)},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or os.getenv(OPENAI_API_KEY_ENV, '')}",
    }
    response = requests.post(OPENAI_CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return {}
    message = choices[0].get("message") or {}
    content = message.get("content") or "{}"
    if isinstance(content, dict):
        return content
    import json
    return json.loads(content)


def normalize_extracted_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {str(key).strip(): value for key, value in (fields or {}).items() if str(key).strip()}
