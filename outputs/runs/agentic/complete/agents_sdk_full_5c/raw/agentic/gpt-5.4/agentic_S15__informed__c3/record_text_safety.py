from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Mapping

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")



def check_text_safety(text: str, attributes: Iterable[str] = DEFAULT_ATTRIBUTES) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    requested = {name: {} for name in attributes}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": requested,
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: payload["summaryScore"]["value"]
        for name, payload in data.get("attributeScores", {}).items()
    }
    return {"provider": "Perspective API", "scores": scores, "raw": data}



def check_record_fields(record: Mapping[str, Any], fields: Iterable[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for field in fields:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            results.append({"field": field, "analysis": check_text_safety(value)})
    return results
