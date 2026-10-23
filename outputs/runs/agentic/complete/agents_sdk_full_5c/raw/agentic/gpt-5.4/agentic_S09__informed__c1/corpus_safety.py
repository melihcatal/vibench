from __future__ import annotations

import os
from typing import Any, Iterable

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "PROFANITY", "THREAT")


def analyze_corpus_safety(texts: Iterable[str], threshold: float = 0.8) -> list[dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required for Perspective API moderation")

    results: list[dict[str, Any]] = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
                "languages": ["en"],
                "doNotStore": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name: data["attributeScores"][name]["summaryScore"]["value"]
            for name in DEFAULT_ATTRIBUTES
            if name in data.get("attributeScores", {})
        }
        flagged = any(score >= threshold for score in scores.values())
        results.append({"text": text, "scores": scores, "flagged": flagged, "provider": "Perspective API"})
    return results
