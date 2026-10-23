from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _normalize_record(record: Any) -> Dict[str, Any]:
    if isinstance(record, dict):
        return record
    if hasattr(record, "model_dump"):
        dumped = record.model_dump()
        if isinstance(dumped, dict):
            return dumped
    if hasattr(record, "dict"):
        dumped = record.dict()
        if isinstance(dumped, dict):
            return dumped
    return {"value": record}


def _extract_records(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [_normalize_record(item) for item in payload]
    if isinstance(payload, dict):
        for key in ("records", "items", "documents", "data", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [_normalize_record(item) for item in value]
        return [_normalize_record(payload)]
    return [_normalize_record(payload)]


def summarize_retrieved_document_records(records: Any, style: Optional[str] = None) -> str:
    normalized = _extract_records(records)
    client = OpenAI()
    prompt = {
        "task": "Summarize retrieved document records concisely and clearly.",
        "style": style or "neutral",
        "records": normalized,
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize document records for end users. Focus on the most important fields, trends, counts, and notable anomalies. Return plain text only.",
            },
            {
                "role": "user",
                "content": json.dumps(prompt, ensure_ascii=False),
            },
        ],
    )
    return getattr(response, "output_text", "") or ""
