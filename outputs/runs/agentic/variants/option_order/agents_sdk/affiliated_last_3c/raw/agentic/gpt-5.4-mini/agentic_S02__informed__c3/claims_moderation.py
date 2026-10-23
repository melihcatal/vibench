from __future__ import annotations

import os
from typing import Iterable

import requests

from identity_models import ModerationResult

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_KEY = os.getenv("PERSPECTIVE_API_KEY", "")


def moderate_claims(text: str, requested_attributes: Iterable[str] = ("TOXICITY", "SEVERE_TOXICITY")) -> ModerationResult:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attribute: {} for attribute in requested_attributes},
        "languages": ["en"],
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={PERSPECTIVE_KEY}", json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    scores = [data.get("attributeScores", {}).get(attr, {}).get("summaryScore", {}).get("value", 0.0) for attr in requested_attributes]
    score = max(scores) if scores else 0.0
    return ModerationResult(text=text, flagged=score >= 0.5, score=score, labels=data)
