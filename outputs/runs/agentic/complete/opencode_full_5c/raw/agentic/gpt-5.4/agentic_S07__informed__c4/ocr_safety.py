from __future__ import annotations

import os

import requests

from document_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = {
    "TOXICITY": {},
    "SEVERE_TOXICITY": {},
    "INSULT": {},
    "PROFANITY": {},
    "THREAT": {},
}


def check_ocr_safety(text: str, threshold: float = 0.7) -> SafetyResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": PERSPECTIVE_ATTRIBUTES,
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= threshold for score in scores.values())
    return SafetyResult(
        provider="perspective-api",
        flagged=flagged,
        scores=scores,
        raw=payload,
    )
