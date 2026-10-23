from __future__ import annotations

import os
import requests

from observability_models import SafetyResult


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str) -> SafetyResult:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return SafetyResult(text=text, is_safe=score < 0.5, reasons=[f"toxicity={score}"])
