from __future__ import annotations

import os
from typing import Dict, List

import requests

from model_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "THREAT",
    "PROFANITY",
    "SEXUALLY_EXPLICIT",
]


def _analyze_text(text: str) -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    flagged: List[str] = []
    for name, payload in data.get("attributeScores", {}).items():
        value = float(payload["summaryScore"]["value"])
        scores[name.lower()] = value
        if value >= 0.7:
            flagged.append(name.lower())
    return SafetyResult(
        provider="perspective",
        blocked=bool(flagged),
        scores=scores,
        flagged_categories=flagged,
    )


def check_prompt_and_output(
    prompt: str, generated_text: str
) -> Dict[str, SafetyResult]:
    return {
        "prompt": _analyze_text(prompt),
        "generated_text": _analyze_text(generated_text),
    }
