from __future__ import annotations

import os
from typing import Any

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_platform_output_safety(text: str, *, languages: list[str] | None = None) -> dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": languages or ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
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
        "safe": max(scores.values(), default=0.0) < 0.7,
        "scores": scores,
        "provider_response": payload,
    }
