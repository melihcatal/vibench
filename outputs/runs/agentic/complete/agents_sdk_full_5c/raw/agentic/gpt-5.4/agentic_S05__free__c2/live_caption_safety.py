from __future__ import annotations

from typing import Any

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_transcript_safety(text: str, api_key: str, language: str = "en") -> dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "languages": [language],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }
    response = requests.post(
        PERSPECTIVE_API_HOST,
        params={"key": api_key},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in (data.get("attributeScores") or {}).items()
    }
    return {"scores": scores, "raw": data}
