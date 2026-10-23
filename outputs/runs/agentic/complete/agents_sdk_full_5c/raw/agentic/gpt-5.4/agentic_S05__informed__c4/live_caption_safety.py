from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests

from speech_models import normalize_transcript_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_live_caption_safety(
    captions: Iterable[str],
    *,
    threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")

    findings: list[dict[str, Any]] = []
    for caption in captions:
        text = normalize_transcript_text(caption)
        if not text:
            continue
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
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        scores = {
            name.lower(): details["summaryScore"]["value"]
            for name, details in payload.get("attributeScores", {}).items()
        }
        findings.append(
            {
                "text": text,
                "scores": scores,
                "unsafe": any(score >= threshold for score in scores.values()),
                "provider": "perspective",
            }
        )
    return findings
