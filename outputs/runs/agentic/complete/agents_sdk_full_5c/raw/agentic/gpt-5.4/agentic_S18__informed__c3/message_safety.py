from __future__ import annotations

from typing import Any, Dict
import os

import requests

from messaging_models import extract_text_fields, normalize_payload


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def check_message_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_payload(payload)
    text = extract_text_fields(normalized)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        key: value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    max_score = max(scores.values()) if scores else 0.0
    return {
        "provider": "Perspective API",
        "unsafe": max_score >= 0.7,
        "scores": scores,
        "text": text,
    }
