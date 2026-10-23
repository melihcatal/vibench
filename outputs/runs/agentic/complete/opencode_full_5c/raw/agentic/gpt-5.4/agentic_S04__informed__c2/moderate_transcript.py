from __future__ import annotations

from typing import Any, Dict

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(
    text: str, languages: list[str] | None = None
) -> Dict[str, Any]:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": languages or ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
