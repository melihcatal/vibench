from __future__ import annotations

import os
from typing import Any

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def check_corpus_safety(
    texts: list[str],
    attributes: list[str] | None = None,
    language: str = "en",
) -> dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise EnvironmentError("PERSPECTIVE_API_KEY is required")
    requested_attributes = attributes or ["TOXICITY", "INSULT", "THREAT"]
    results = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": [language],
                "requestedAttributes": {name: {} for name in requested_attributes},
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        scores = {
            name: value["summaryScore"]["value"]
            for name, value in payload.get("attributeScores", {}).items()
        }
        results.append({"text": text, "scores": scores, "flagged": any(score >= 0.7 for score in scores.values())})
    return {"provider": "Perspective API", "results": results}
