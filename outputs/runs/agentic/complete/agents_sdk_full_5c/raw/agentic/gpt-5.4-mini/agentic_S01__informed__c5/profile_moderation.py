from __future__ import annotations

import os

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(text: str):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    attrs = data.get("attributeScores", {})
    toxicity = attrs.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    labels = {k: v.get("summaryScore", {}).get("value", 0.0) for k, v in attrs.items()}
    return ModerationResult(allowed=toxicity < 0.7, score=toxicity, labels=labels, raw=data)
