import json
import os
from typing import Any, Dict, Iterable, List, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def _score_confidence(value: Any) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    if isinstance(value, str):
        lowered = value.strip().lower()
        mapping = {"high": 0.9, "medium": 0.6, "low": 0.3, "certain": 1.0, "uncertain": 0.2}
        if lowered in mapping:
            return mapping[lowered]
    return 0.0


def validate_document_fields(document: Dict[str, Any], required_fields: Iterable[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    missing: List[str] = []
    low_confidence: List[Tuple[str, float]] = []

    for field in required_fields:
        if field not in document or document[field] in (None, "", [], {}, ()):
            missing.append(field)
            continue

        confidence_field = f"{field}_confidence"
        if confidence_field in document:
            confidence = _score_confidence(document[confidence_field])
            if confidence < min_confidence:
                low_confidence.append((field, confidence))

    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
    }


def validate_with_openai(document_text: str, required_fields: Iterable[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = {
        "required_fields": list(required_fields),
        "min_confidence": min_confidence,
        "document": document_text,
        "task": "Return JSON with fields present and confidence scores from 0 to 1 for each required field.",
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Extract structured fields and confidence scores as JSON only."},
                {"role": "user", "content": json.dumps(prompt)},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return _extract_json(content)


__all__ = ["validate_document_fields", "validate_with_openai"]
