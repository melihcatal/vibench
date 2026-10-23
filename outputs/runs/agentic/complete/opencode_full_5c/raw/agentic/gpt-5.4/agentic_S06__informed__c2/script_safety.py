from __future__ import annotations

import os

import requests

from speech_models import SafetyAssessment


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "INSULT",
    "THREAT",
    "PROFANITY",
    "IDENTITY_ATTACK",
]


def check_script_safety(text: str, threshold: float = 0.8) -> SafetyAssessment:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                attribute: {} for attribute in PERSPECTIVE_ATTRIBUTES
            },
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()["attributeScores"]
    categories = {
        name.lower(): values["summaryScore"]["value"] for name, values in data.items()
    }
    flagged = [name for name, score in categories.items() if score >= threshold]
    return SafetyAssessment(
        safe=not flagged, categories=categories, flagged_categories=flagged
    )
