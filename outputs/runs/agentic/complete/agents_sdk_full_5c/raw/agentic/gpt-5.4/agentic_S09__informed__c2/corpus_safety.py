from __future__ import annotations

import os
from typing import Any, Iterable

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_corpus_safety(texts: Iterable[str], *, threshold: float = 0.7) -> list[dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required for Perspective API moderation")
    findings: list[dict[str, Any]] = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
            "languages": ["en"],
        }
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name: data["attributeScores"][name]["summaryScore"]["value"]
            for name in DEFAULT_ATTRIBUTES
            if name in data.get("attributeScores", {})
        }
        findings.append(
            {
                "text": text,
                "scores": scores,
                "blocked": any(value >= threshold for value in scores.values()),
            }
        )
    return findings
