from __future__ import annotations

import os
from typing import Any, Dict

import requests

from observability_models import SafetyResult


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_HOST,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    scores = {name.lower(): float(payload["summaryScore"]["value"]) for name, payload in data.items()}
    flagged = [name for name, score in scores.items() if score >= 0.7]
    result = SafetyResult(is_safe=not flagged, scores=scores, flagged_categories=flagged)
    return result.__dict__
