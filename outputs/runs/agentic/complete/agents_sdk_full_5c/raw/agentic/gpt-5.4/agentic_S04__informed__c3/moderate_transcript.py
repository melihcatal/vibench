from __future__ import annotations

import os
from typing import Iterable, List, Sequence

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(segments: Sequence[str] | Iterable[str], threshold: float = 0.7) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    texts: List[str] = [segment for segment in segments if segment]
    findings = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        scores = {
            name.lower(): values["summaryScore"]["value"]
            for name, values in payload.get("attributeScores", {}).items()
        }
        flagged = any(score >= threshold for score in scores.values())
        findings.append({"text": text, "scores": scores, "flagged": flagged})
    return {
        "provider": "Perspective API",
        "endpoint": PERSPECTIVE_API_URL,
        "threshold": threshold,
        "results": findings,
    }
