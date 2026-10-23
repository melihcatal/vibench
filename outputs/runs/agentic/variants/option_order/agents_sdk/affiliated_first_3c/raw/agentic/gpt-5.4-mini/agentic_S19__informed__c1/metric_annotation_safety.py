from __future__ import annotations

from typing import Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str, api_key: str) -> Dict[str, object]:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {"unsafe": any(scores.get(attr, {}).get("summaryScore", {}).get("value", 0) >= 0.5 for attr in ["TOXICITY", "INSULT", "PROFANITY"]), "scores": scores, "provider": "Perspective API"}
