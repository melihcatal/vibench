from __future__ import annotations

import os
from typing import Any, Dict

import requests


def log_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
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
    return response.json()
