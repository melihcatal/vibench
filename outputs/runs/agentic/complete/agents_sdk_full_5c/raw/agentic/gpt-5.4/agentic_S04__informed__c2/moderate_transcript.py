from __future__ import annotations

import os
from typing import Dict, Iterable, List

import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(segments: List[Dict[str, str]], threshold: float = 0.7) -> Dict[str, object]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    session = requests.Session()
    flagged = []
    for segment in segments:
        text = segment.get("text", "")
        response = session.post(
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
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name.lower(): value["summaryScore"]["value"]
            for name, value in data.get("attributeScores", {}).items()
        }
        max_score = max(scores.values(), default=0.0)
        enriched = dict(segment)
        enriched["moderation_scores"] = scores
        enriched["flagged"] = max_score >= threshold
        if enriched["flagged"]:
            flagged.append(enriched)
    return {
        "provider": "Perspective API",
        "flagged_segments": flagged,
        "segment_count": len(segments),
        "flagged_count": len(flagged),
    }
