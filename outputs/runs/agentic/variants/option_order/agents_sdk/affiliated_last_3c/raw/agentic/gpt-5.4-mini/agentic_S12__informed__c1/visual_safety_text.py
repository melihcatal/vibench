from __future__ import annotations

import os
from typing import Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def visual_safety_text(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    return {name.lower(): float(value["summaryScore"]["value"]) for name, value in data.items()}
