from __future__ import annotations

import os
from typing import Dict, List, Sequence

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(
    segments: Sequence[str],
    languages: Sequence[str] | None = None,
    attributes: Sequence[str] | None = None,
) -> Dict[str, List[Dict[str, object]]]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    requested_attributes = attributes or ["TOXICITY", "INSULT", "PROFANITY"]
    results: List[Dict[str, object]] = []
    for text in segments:
        payload = {
            "comment": {"text": text},
            "languages": list(languages or ["en"]),
            "requestedAttributes": {name: {} for name in requested_attributes},
        }
        response = requests.post(
            f"{PERSPECTIVE_API_URL}?key={api_key}",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            key: value["summaryScore"]["value"]
            for key, value in data.get("attributeScores", {}).items()
        }
        results.append({"text": text, "scores": scores})
    return {
        "provider": "Perspective API",
        "results": results,
    }
