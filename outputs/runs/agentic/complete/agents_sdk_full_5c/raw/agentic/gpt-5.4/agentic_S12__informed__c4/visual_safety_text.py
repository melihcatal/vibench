from __future__ import annotations

import os
from typing import Iterable, List

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_visual_labels_for_unsafe_text(labels: Iterable[str], languages: List[str] | None = None) -> dict:
    text = ", ".join(label for label in labels if label)
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": os.getenv("PERSPECTIVE_API_KEY")},
        json={
            "comment": {"text": text},
            "languages": languages or ["en"],
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
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "model": "commentanalyzer-v1alpha1",
        "input_text": text,
        "scores": scores,
        "raw_response": data,
    }
