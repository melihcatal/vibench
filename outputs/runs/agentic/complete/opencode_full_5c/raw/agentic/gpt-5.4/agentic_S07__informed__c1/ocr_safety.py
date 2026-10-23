from __future__ import annotations

import requests

from document_client import get_perspective_api_key
from document_models import SafetyCheckResult


def check_ocr_text_safety(text: str) -> SafetyCheckResult:
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": get_perspective_api_key()},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return SafetyCheckResult(
        provider="perspective-api", flagged=flagged, scores=scores, raw=payload
    )
