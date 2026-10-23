from __future__ import annotations

import os
from typing import Any

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_safety(
    text: str,
    *,
    languages: list[str] | None = None,
    requested_attributes: dict[str, Any] | None = None,
    do_not_store: bool = True,
) -> dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required for Perspective API moderation")

    payload = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": requested_attributes or {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": do_not_store,
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
        name: details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    return {
        "provider": "Perspective API",
        "scores": scores,
        "flagged": any(score >= 0.7 for score in scores.values()),
        "raw": data,
    }
