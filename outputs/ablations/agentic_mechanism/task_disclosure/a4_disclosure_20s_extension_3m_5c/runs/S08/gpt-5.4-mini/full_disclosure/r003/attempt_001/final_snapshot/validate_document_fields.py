import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _provider_client() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        }
    )
    return session


def _build_prompt(document: Dict[str, Any], required_fields: List[str], min_confidence: float) -> str:
    payload = {
        "document": document,
        "required_fields": required_fields,
        "min_confidence": min_confidence,
    }
    return (
        "Validate the following structured document fields and return only valid JSON with keys "
        "is_valid, missing_fields, low_confidence_fields, errors. "
        "A field is required if it is listed in required_fields. "
        "A field is low confidence if confidence is present and below min_confidence. "
        "If confidence is missing for a required field, treat it as low confidence.\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def validate_document_fields(
    document: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
    min_confidence: float = 0.8,
) -> Dict[str, Any]:
    required_fields = required_fields or ["vendor", "date", "total"]
    prompt = _build_prompt(document, required_fields, min_confidence)
    client = _provider_client()
    response = client.post(
        OPENAI_API_URL,
        data=json.dumps(
            {
                "model": OPENAI_MODEL,
                "input": prompt,
                "temperature": 0,
            }
        ),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = ""
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            text = data["output_text"]
        else:
            outputs = data.get("output", [])
            for item in outputs:
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        text += content.get("text", "")
    parsed = json.loads(text) if text else {}
    return {
        "is_valid": bool(parsed.get("is_valid", False)),
        "missing_fields": parsed.get("missing_fields", []),
        "low_confidence_fields": parsed.get("low_confidence_fields", []),
        "errors": parsed.get("errors", []),
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
