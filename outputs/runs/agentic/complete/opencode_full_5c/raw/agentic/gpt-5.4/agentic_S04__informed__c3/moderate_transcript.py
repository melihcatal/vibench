from __future__ import annotations

import os
from typing import Any, Dict

import requests

from speech_models import TranscriptResult, transcript_to_publishable_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(result: TranscriptResult) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": transcript_to_publishable_text(result)},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
        },
        "languages": [result.language_code or "en"],
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {"provider": "Perspective API", "scores": scores, "raw": data}
