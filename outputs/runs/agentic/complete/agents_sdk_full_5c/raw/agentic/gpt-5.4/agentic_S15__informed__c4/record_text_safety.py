from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_text_safety(texts: Iterable[str], language: str = "en") -> List[Dict[str, Any]]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    results: List[Dict[str, Any]] = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": [language],
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
        results.append({"text": text, "scores": scores, "provider": "Perspective API"})
    return results
