from __future__ import annotations

import os
from typing import Iterable, List

import requests


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_labels_safety(labels: Iterable[str]) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API")

    joined_text = ", ".join(label for label in labels if label)
    response = requests.post(
        PERSPECTIVE_URL,
        params={"key": api_key},
        json={
            "comment": {"text": joined_text},
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
    payload = response.json()
    scores = {
        name.lower(): data["summaryScore"]["value"]
        for name, data in payload.get("attributeScores", {}).items()
    }
    max_score = max(scores.values(), default=0.0)
    return {
        "provider": "perspective-api",
        "scores": scores,
        "unsafe": max_score >= 0.7,
        "analyzed_text": joined_text,
    }
