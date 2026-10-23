from __future__ import annotations

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_caption_safety(text: str, attributes: list[str] | None = None) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API")
    requested_attributes = attributes or ["TOXICITY", "INSULT", "THREAT"]
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in requested_attributes},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name: payload["attributeScores"][name]["summaryScore"]["value"]
        for name in requested_attributes
        if name in payload.get("attributeScores", {})
    }
    return {"text": text, "scores": scores, "raw": payload}
