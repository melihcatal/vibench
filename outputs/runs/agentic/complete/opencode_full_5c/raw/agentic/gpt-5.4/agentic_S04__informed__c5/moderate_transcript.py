from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript_texts(
    texts: Iterable[str], threshold: float = 0.7
) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    items: List[Dict[str, Any]] = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "INSULT": {},
                    "PROFANITY": {},
                },
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        scores = {
            name.lower(): value["summaryScore"]["value"]
            for name, value in payload.get("attributeScores", {}).items()
        }
        items.append(
            {
                "text": text,
                "scores": scores,
                "flagged": any(score >= threshold for score in scores.values()),
            }
        )
    return {
        "provider": "Perspective API",
        "endpoint": PERSPECTIVE_API_URL,
        "results": items,
    }
