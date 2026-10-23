from __future__ import annotations

import os

import requests


def visual_safety_text(
    labels: list[str] | str, languages: list[str] | None = None
) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    text = ", ".join(labels) if isinstance(labels, list) else labels
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": languages or ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return {"flagged": flagged, "scores": scores, "provider": "Perspective API"}
