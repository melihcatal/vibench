from __future__ import annotations

from typing import Tuple

import requests

from identity_models import ModerationResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = "${PERSPECTIVE_API_KEY}"


def moderate_claims_text(text: str) -> ModerationResult:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    label = "flagged" if score >= 0.5 else "clean"
    return ModerationResult(text=text, label=label, score=score, reasons=["Perspective API toxicity"])
