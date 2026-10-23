from __future__ import annotations

import os
from typing import Dict

import requests

from translation_models import UnsafeContentResult


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def unsafe_copy_check(text: str) -> UnsafeContentResult:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    payload: Dict[str, object] = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(f"{PERSPECTIVE_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    attrs = data.get("attributeScores", {})
    scores = [float(attrs[name]["summaryScore"]["value"]) for name in attrs if "summaryScore" in attrs[name]]
    score = max(scores) if scores else 0.0
    labels = [name.lower() for name in attrs if float(attrs[name]["summaryScore"]["value"]) >= 0.5]
    return UnsafeContentResult(flagged=bool(labels), provider="perspective-api", score=score, labels=labels, details=data)
