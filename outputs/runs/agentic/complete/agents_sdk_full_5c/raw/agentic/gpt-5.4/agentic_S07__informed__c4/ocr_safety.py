from __future__ import annotations

import os

import requests

from document_models import normalize_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_ocr_safety(text: str, language: str = "en") -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": normalize_text(text)},
            "languages": [language],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
            "doNotStore": True,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name: payload["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in payload.get("attributeScores", {})
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "raw": payload,
    }
