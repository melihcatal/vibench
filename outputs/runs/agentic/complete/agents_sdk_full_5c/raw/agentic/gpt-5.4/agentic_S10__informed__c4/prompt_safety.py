from __future__ import annotations

import os
from typing import Dict, List

import requests

from model_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "SEXUALLY_EXPLICIT"]


def check_prompt_safety(text: str, threshold: float = 0.8) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    requested_attributes: Dict[str, Dict[str, str]] = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": requested_attributes,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name: payload.get("attributeScores", {}).get(name, {}).get("summaryScore", {}).get("value", 0.0)
        for name in DEFAULT_ATTRIBUTES
    }
    flagged: List[str] = [name for name, score in scores.items() if score >= threshold]
    return SafetyResult(provider="Perspective API", unsafe=bool(flagged), scores=scores, flagged_segments=flagged)
