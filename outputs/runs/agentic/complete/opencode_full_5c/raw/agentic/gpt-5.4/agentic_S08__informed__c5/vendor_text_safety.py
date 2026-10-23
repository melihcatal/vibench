from __future__ import annotations

import os
from typing import Any, Dict

import requests


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    response = requests.post(
        endpoint,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return {"provider": "perspective-api", "flagged": flagged, "scores": scores}
