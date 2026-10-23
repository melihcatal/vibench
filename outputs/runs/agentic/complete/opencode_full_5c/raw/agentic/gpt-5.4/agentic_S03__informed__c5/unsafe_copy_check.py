from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def unsafe_copy_check(text: str, language: str | None = None) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": [language] if language else None,
    }
    body = {key: value for key, value in body.items() if value is not None}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    return {"provider": "Perspective API", "scores": scores, "raw": data}
