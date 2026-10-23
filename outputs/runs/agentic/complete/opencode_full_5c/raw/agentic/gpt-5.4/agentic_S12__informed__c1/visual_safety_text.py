from __future__ import annotations

import os
from typing import Iterable

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def visual_safety_text(labels: Iterable[str]) -> dict:
    text = ", ".join(label for label in labels if label)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in payload.get("attributeScores", {}).items()
    }
    return {
        "provider": "perspective-api",
        "scores": scores,
        "is_unsafe": any(score >= 0.7 for score in scores.values()),
    }
