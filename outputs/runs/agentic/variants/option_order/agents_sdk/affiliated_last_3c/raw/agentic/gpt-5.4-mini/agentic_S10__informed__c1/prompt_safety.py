from __future__ import annotations

import os
from typing import Dict

import requests

from model_models import ModerationResult, normalize_text

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt_safety(text: str) -> ModerationResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload: Dict[str, object] = {
        "comment": {"text": normalize_text(text)},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    params = {"key": api_key}
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = {}
    for name, attr in data.get("attributeScores", {}).items():
        scores[name.lower()] = float(attr.get("summaryScore", {}).get("value", 0.0))
    flagged = any(score >= 0.7 for score in scores.values())
    return ModerationResult(provider="Perspective API", flagged=flagged, scores=scores, raw=data)
