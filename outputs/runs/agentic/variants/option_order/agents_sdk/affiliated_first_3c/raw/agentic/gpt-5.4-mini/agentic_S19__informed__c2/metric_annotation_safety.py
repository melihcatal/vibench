from __future__ import annotations

import os
from typing import Any, Dict

import requests

PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API access")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": ["en"],
    }
    response = requests.post(f"{PERSPECTIVE_API_BASE}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    unsafe = any(scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0) >= 0.5 for attr in scores)
    return {"text": text, "unsafe": unsafe, "scores": scores, "raw": data}
