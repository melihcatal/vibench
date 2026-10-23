from __future__ import annotations

import os
from typing import Dict, Iterable, List

import requests


PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


_DEFAULT_ATTRIBUTES = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT"]


def moderate_transcript(segments: Iterable[Dict[str, object]], threshold: float = 0.7) -> Dict[str, object]:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    flagged: List[Dict[str, object]] = []
    all_results: List[Dict[str, object]] = []
    for segment in segments:
        text = str(segment.get("text", ""))
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in _DEFAULT_ATTRIBUTES},
        }
        response = requests.post(
            f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name: data["attributeScores"][name]["summaryScore"]["value"]
            for name in _DEFAULT_ATTRIBUTES
            if name in data.get("attributeScores", {})
        }
        item = {**segment, "scores": scores}
        all_results.append(item)
        if any(score >= threshold for score in scores.values()):
            flagged.append(item)
    return {
        "provider": "Perspective API",
        "threshold": threshold,
        "results": all_results,
        "flagged": flagged,
    }
