from __future__ import annotations

import os
from typing import Dict, Iterable

import requests

from model_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY", "SEXUALLY_EXPLICIT")


def _analyze_text(text: str, attributes: Iterable[str]) -> Dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    requested = {name: {} for name in attributes}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": requested,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_prompt_safety(prompt: str, generated_text: str = "") -> SafetyCheckResult:
    combined = prompt if not generated_text else f"Prompt:\n{prompt}\n\nGenerated:\n{generated_text}"
    data = _analyze_text(combined, DEFAULT_ATTRIBUTES)
    scores = {
        name.lower(): values["summaryScore"]["value"]
        for name, values in data.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyCheckResult(
        flagged=flagged,
        provider="Perspective API",
        scores=scores,
        details=data,
    )
