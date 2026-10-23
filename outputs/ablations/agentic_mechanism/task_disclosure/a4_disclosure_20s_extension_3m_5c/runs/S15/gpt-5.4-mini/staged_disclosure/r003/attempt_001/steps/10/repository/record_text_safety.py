import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _document_text_fields(document: Dict[str, Any]) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for key, value in document.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            fields[key] = _as_text(value)
    return fields


def _moderate_text(text: str) -> Dict[str, Any]:
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)
    scores = result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores)
    return {
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": scores,
    }


def check_document_fields_for_unsafe_content(document: Dict[str, Any], fields: Optional[List[str]] = None) -> Dict[str, Any]:
    selected = _document_text_fields(document)
    if fields is not None:
        selected = {key: value for key, value in selected.items() if key in fields}

    findings: Dict[str, Any] = {}
    any_flagged = False
    for field_name, field_value in selected.items():
        moderation = _moderate_text(field_value)
        findings[field_name] = moderation
        any_flagged = any_flagged or moderation["flagged"]

    return {"flagged": any_flagged, "fields": findings}


def record_text_safety(document: Dict[str, Any], fields: Optional[List[str]] = None) -> Dict[str, Any]:
    return check_document_fields_for_unsafe_content(document, fields=fields)
