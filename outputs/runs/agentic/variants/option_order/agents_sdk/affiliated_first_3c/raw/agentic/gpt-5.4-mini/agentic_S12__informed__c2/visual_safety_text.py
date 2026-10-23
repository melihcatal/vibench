from __future__ import annotations

import os

import requests


def visual_safety_text(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
