import os
from typing import Any, Dict

from openai import OpenAI

from document_models import StructuredDocumentRequest, StructuredDocumentResponse, StructuredDocumentField, normalize_line_items


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_model_name() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")


def extract_structured_document(prompt: str, request: StructuredDocumentRequest) -> StructuredDocumentResponse:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": request.document_text},
        ],
        text={"format": {"type": "json_object"}},
    )
    payload: Dict[str, Any] = getattr(response, "output_parsed", None) or {}
    fields = {}
    for key, value in payload.items():
        if key == "line_items":
            value = normalize_line_items(value)
        if isinstance(value, dict) and "value" in value:
            fields[key] = StructuredDocumentField(
                value=value.get("value"),
                confidence=float(value.get("confidence", 0.0)),
                source=value.get("source"),
            )
        else:
            fields[key] = StructuredDocumentField(value=value, confidence=1.0)
    return StructuredDocumentResponse(fields=fields, raw=payload)


def merge_field_maps(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    merged.update(updates)
    return merged
