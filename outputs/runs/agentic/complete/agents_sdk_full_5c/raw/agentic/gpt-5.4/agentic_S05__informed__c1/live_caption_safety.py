from __future__ import annotations

import os
from typing import Dict

import requests

from speech_models import CaptionSafetyResult, normalize_transcript_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_live_caption_safety(text: str, threshold: float = 0.8) -> CaptionSafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY for Perspective API")
    normalized = normalize_transcript_text(text)
    payload = {
        "comment": {"text": normalized},
        "languages": ["en"],
        "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {
        name: data["attributeScores"][name]["summaryScore"]["value"] for name in DEFAULT_ATTRIBUTES
    }
    unsafe = any(score >= threshold for score in scores.values())
    return CaptionSafetyResult(text=normalized, unsafe=unsafe, scores=scores, raw=data)
