import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _as_dict(document: Any) -> Dict[str, Any]:
    if isinstance(document, dict):
        return document
    if isinstance(document, str):
        try:
            parsed = json.loads(document)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _required_fields() -> List[str]:
    return ["document_id", "document_type", "issue_date", "confidence_scores"]


def _confidence_scores(document: Dict[str, Any]) -> Dict[str, Any]:
    scores = document.get("confidence_scores")
    return scores if isinstance(scores, dict) else {}


def validate_document_fields(document: Any, min_confidence: float = 0.8) -> Dict[str, Any]:
    payload = _as_dict(document)
    missing_fields = [field for field in _required_fields() if field not in payload or payload[field] in (None, "")]
    confidence_scores = _confidence_scores(payload)
    low_confidence_fields = {
        field: score
        for field, score in confidence_scores.items()
        if isinstance(score, (int, float)) and score < min_confidence
    }
    non_numeric_confidence_fields = {
        field: score
        for field, score in confidence_scores.items()
        if not isinstance(score, (int, float))
    }
    valid = not missing_fields and not low_confidence_fields and not non_numeric_confidence_fields
    return {
        "valid": valid,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "non_numeric_confidence_fields": non_numeric_confidence_fields,
    }


def validate_document_fields_with_openai(document: Any, min_confidence: float = 0.8) -> Dict[str, Any]:
    payload = _as_dict(document)
    response = _client().responses.create(
        model=DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Validate structured document fields and confidence scores.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "document": payload,
                        "min_confidence": min_confidence,
                        "required_fields": _required_fields(),
                    }
                ),
            },
        ],
    )
    text = getattr(response, "output_text", "") or ""
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {}
    if not isinstance(result, dict):
        result = {}
    result.setdefault("provider", "openai")
    result.setdefault("model", DEFAULT_MODEL)
    return result


__all__ = ["validate_document_fields", "validate_document_fields_with_openai"]
