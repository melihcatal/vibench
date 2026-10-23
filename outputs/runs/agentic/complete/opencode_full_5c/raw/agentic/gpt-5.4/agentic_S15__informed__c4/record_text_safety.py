from __future__ import annotations

import os
from typing import Any

import requests


def check_record_text_safety(text_fields: dict[str, Any]) -> dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    joined_text = "\n".join(
        str(value) for value in text_fields.values() if value is not None
    )
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": joined_text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in payload.get("attributeScores", {}).items()
    }
    max_score = max(scores.values(), default=0.0)
    return {
        "provider": "perspective_api",
        "unsafe": max_score >= 0.7,
        "scores": scores,
    }
