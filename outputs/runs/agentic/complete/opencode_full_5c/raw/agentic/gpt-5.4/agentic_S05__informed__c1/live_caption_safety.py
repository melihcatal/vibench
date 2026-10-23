from __future__ import annotations

import os

import requests

from speech_models import normalize_caption_chunk


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_live_caption_safety(text: str) -> dict[str, float]:
    normalized = normalize_caption_chunk(text)
    if not normalized:
        return {}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": normalized},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    return {
        name.lower(): scores["summaryScore"]["value"]
        for name, scores in data.items()
        if "summaryScore" in scores
    }
