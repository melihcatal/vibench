from __future__ import annotations

import requests

from security_client import get_perspective_api_key
from security_models import SafetyAssessment, normalize_labels_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def secret_label_safety(labels, notes: str) -> SafetyAssessment:
    text = normalize_labels_text(labels, notes)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": get_perspective_api_key()},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name.lower(): value["summaryScore"]["value"]
        for name, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    unsafe_terms = [name for name, score in scores.items() if score >= 0.7]
    return SafetyAssessment(
        text=text, flagged=flagged, categories=scores, unsafe_terms=unsafe_terms
    )
