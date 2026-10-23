from __future__ import annotations

import os
from typing import Dict

import requests

from observability_models import AnnotationSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(
    text: str, languages: list[str] | None = None
) -> AnnotationSafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
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
    scores: Dict[str, float] = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    is_safe = all(score < 0.7 for score in scores.values())
    return AnnotationSafetyResult(
        is_safe=is_safe, flagged_categories=scores, provider="Perspective API"
    )
