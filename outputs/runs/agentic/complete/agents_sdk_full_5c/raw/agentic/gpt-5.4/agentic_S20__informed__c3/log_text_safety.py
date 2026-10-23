from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_text_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_HOST,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": [language],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
