import json
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _text_from_response(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    parts: List[str] = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            value = getattr(content, "text", None)
            if value:
                parts.append(value)
    return "".join(parts)


def _validation_prompt(document_fields: Dict[str, Any]) -> str:
    return (
        "Validate required structured document fields and confidence scores for an expense document. "
        "Return valid JSON only with keys valid, missing_fields, low_confidence_fields, and issues. "
        "Treat required fields as vendor, date, and total for invoices, or merchant, date, and total for receipts. "
        "A field is low confidence when its confidence value is present and below 0.80. "
        "If confidence values are nested per field, inspect them directly. "
        "Document fields:\n"
        f"{json.dumps(document_fields, ensure_ascii=False)}"
    )


def validate_document_fields(document_fields: Dict[str, Any]) -> Dict[str, Any]:
    response = _client().responses.create(
        model=OPENAI_MODEL,
        input=_validation_prompt(document_fields),
        temperature=0,
    )
    return json.loads(_text_from_response(response))


def validate_document_fields_from_json(document_json: str) -> Dict[str, Any]:
    return validate_document_fields(json.loads(document_json))


__all__ = ["validate_document_fields", "validate_document_fields_from_json"]
