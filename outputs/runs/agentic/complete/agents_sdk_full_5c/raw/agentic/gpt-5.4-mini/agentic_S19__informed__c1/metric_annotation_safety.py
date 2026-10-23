from __future__ import annotations

import os

import requests

from observability_models import AnnotationSafetyResult, normalize_text

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_annotation_safety(text: str) -> AnnotationSafetyResult:
    normalized = normalize_text(text)
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": normalized},
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = [
        data.get("attributeScores", {}).get(attr, {}).get("summaryScore", {}).get("value", 0.0)
        for attr in ("TOXICITY", "INSULT", "THREAT")
    ]
    risk = max(scores) if scores else 0.0
    return AnnotationSafetyResult(text=normalized, safe=risk < 0.5, risk_score=risk, provider_result=data)
