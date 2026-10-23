from __future__ import annotations

import os
from typing import Iterable

import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims_text(text: str, requested_attributes: Iterable[str] | None = None) -> dict:
    attributes = list(requested_attributes or ["TOXICITY", "INSULT", "PROFANITY"])
    if not PERSPECTIVE_API_KEY:
        return {"moderated": False, "reason": "missing api key", "text": text, "attributes": attributes}
    response = requests.post(
        f"{PERSPECTIVE_ENDPOINT}?key={PERSPECTIVE_API_KEY}",
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {attr: {} for attr in attributes},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
