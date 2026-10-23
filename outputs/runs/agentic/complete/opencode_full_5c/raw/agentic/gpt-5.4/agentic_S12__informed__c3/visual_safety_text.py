from __future__ import annotations

import os

import requests

from vision_models import TextSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_labels_safety(text: str, threshold: float = 0.7) -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    result = TextSafetyResult(
        provider="perspective-api",
        flagged=flagged,
        scores=scores,
        raw_response=data,
    )
    return result.to_dict()
