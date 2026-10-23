from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import SafetyResult, normalize_text

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_script_safety(text: str) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload: Dict[str, object] = {
        "comment": {"text": normalize_text(text)},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = float(data["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
    return SafetyResult(text=text, provider="Perspective API", flagged=score >= 0.5, categories={"toxicity": score}, metadata=data)
