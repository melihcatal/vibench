from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"



def check_text_safety(texts: Iterable[str], threshold: float = 0.8) -> List[Dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")

    findings: List[Dict[str, Any]] = []
    for text in texts:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": api_key},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        scores = {
            name.lower(): details["summaryScore"]["value"]
            for name, details in data.get("attributeScores", {}).items()
        }
        findings.append(
            {
                "text": text,
                "scores": scores,
                "flagged": any(score >= threshold for score in scores.values()),
            }
        )
    return findings
