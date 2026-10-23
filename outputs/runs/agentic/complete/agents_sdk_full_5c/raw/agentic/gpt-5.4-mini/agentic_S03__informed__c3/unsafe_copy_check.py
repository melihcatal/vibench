from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_copy(text: str) -> SafetyCheckResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": ["en"],
    }
    response = requests.post(
        f"{PERSPECTIVE_API_HOST}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    labels = {
        key.lower(): float(value["summaryScore"]["value"])
        for key, value in data.get("attributeScores", {}).items()
    }
    is_safe = all(score < 0.5 for score in labels.values())
    return SafetyCheckResult(provider="Perspective API", is_safe=is_safe, labels=labels, metadata={"host": PERSPECTIVE_API_HOST})
