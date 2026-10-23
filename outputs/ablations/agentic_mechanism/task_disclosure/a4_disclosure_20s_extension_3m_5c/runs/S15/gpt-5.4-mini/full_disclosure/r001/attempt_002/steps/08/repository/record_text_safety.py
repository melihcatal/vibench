from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"


def _extract_text_fields(record: Any) -> str:
    if record is None:
        return ""
    if isinstance(record, str):
        return record
    if isinstance(record, (int, float, bool)):
        return str(record)
    if isinstance(record, list):
        parts = [_extract_text_fields(item) for item in record]
        return "\n".join(part for part in parts if part)
    if isinstance(record, dict):
        preferred_keys = (
            "text",
            "content",
            "body",
            "message",
            "title",
            "description",
            "summary",
            "comment",
            "notes",
        )
        parts: List[str] = []
        for key in preferred_keys:
            if key in record and record[key] is not None:
                value = _extract_text_fields(record[key])
                if value:
                    parts.append(value)
        if parts:
            return "\n".join(parts)
        return "\n".join(
            part for part in (_extract_text_fields(value) for value in record.values()) if part
        )
    return str(record)


def _normalize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    result = data.get("results", [{}])[0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, value in categories.items() if value]
    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "categories": categories,
        "category_scores": category_scores,
    }


def check_text_safety(record: Any, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    text = _extract_text_fields(record).strip()
    if not text:
        return {
            "flagged": False,
            "unsafe_categories": [],
            "categories": {},
            "category_scores": {},
        }

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for moderation checks")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return _normalize_response(response.json())


def check_documents_safety(records: Iterable[Any], model: str = "omni-moderation-latest") -> List[Dict[str, Any]]:
    return [check_text_safety(record, model=model) for record in records]


def handler(event: Any, context: Any = None) -> Dict[str, Any]:
    if isinstance(event, str):
        payload = json.loads(event)
    else:
        payload = event or {}
    record = payload.get("record", payload)
    return check_text_safety(record, model=payload.get("model", "omni-moderation-latest"))
