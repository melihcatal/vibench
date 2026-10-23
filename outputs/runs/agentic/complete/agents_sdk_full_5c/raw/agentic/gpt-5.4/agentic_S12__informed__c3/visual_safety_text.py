from __future__ import annotations

import os
from typing import Dict

import requests

from vision_models import TextSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_labels_text_safety(text: str) -> TextSafetyResult:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
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
    data = response.json()
    scores: Dict[str, float] = {}
    for name, payload in data.get("attributeScores", {}).items():
        scores[name.lower()] = float(payload["summaryScore"]["value"])
    flagged = any(value >= 0.7 for value in scores.values())
    return TextSafetyResult(flagged=flagged, scores=scores, provider="perspective-api")
