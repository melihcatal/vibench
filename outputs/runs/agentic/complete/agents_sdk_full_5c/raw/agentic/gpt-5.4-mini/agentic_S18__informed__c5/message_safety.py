from __future__ import annotations

from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str, api_key: str | None = None) -> Dict[str, Any]:
    params = {"key": api_key or __import__("os").getenv("PERSPECTIVE_API_KEY", "")}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
        "doNotStore": True,
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {
        "unsafe": any(float(v.get("summaryScore", {}).get("value", 0.0)) >= 0.7 for v in scores.values()),
        "scores": scores,
        "provider": "Perspective API",
    }
