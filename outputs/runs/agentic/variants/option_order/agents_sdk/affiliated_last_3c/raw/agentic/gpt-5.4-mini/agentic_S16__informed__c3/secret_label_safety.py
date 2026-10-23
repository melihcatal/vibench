from __future__ import annotations

from typing import Dict

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def secret_label_safety(text: str, api_key: str) -> Dict[str, float]:
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "PROFANITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {
        name.lower(): float(score.get("summaryScore", {}).get("value", 0.0))
        for name, score in scores.items()
    }
