from __future__ import annotations

import os
from typing import Dict

import requests

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com"


def check_annotation_safety(text: str) -> Dict[str, float | bool]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    url = f"{PERSPECTIVE_API_HOST}/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
        "languages": ["en"],
    }
    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    insult = scores.get("INSULT", {}).get("summaryScore", {}).get("value", 0.0)
    profanity = scores.get("PROFANITY", {}).get("summaryScore", {}).get("value", 0.0)
    return {"safe": max(toxicity, insult, profanity) < 0.5, "toxicity": toxicity, "insult": insult, "profanity": profanity}
