from __future__ import annotations

import os
from typing import List

import requests

from model_models import SafetyResult

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(text: str) -> SafetyResult:
    key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}, "IDENTITY_ATTACK": {}},
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    categories: List[str] = []
    for name, payload_item in data.get("attributeScores", {}).items():
        summary = payload_item.get("summaryScore", {}).get("value", 0.0)
        if summary >= 0.5:
            categories.append(name.lower())
    return SafetyResult(flagged=bool(categories), categories=categories, raw=data)
