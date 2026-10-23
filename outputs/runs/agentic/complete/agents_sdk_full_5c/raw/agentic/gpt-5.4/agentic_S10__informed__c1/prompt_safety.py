from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_prompt_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: data["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in data.get("attributeScores", {})
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return {"provider": "Perspective API", "flagged": flagged, "scores": scores, "raw": data}
