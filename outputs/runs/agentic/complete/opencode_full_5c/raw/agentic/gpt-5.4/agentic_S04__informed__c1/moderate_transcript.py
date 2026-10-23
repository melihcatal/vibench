from __future__ import annotations

from typing import Dict, List

import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(segments: List[Dict[str, str]]) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    moderated = []
    for segment in segments:
        text = segment.get("text", "")
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
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
        data = response.json()
        scores = {
            name.lower(): value["summaryScore"]["value"]
            for name, value in data.get("attributeScores", {}).items()
        }
        item = dict(segment)
        item["moderation_scores"] = scores
        item["flagged"] = any(score >= 0.8 for score in scores.values())
        moderated.append(item)
    return {
        "provider": "Perspective API",
        "segments": moderated,
    }
