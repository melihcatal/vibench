from __future__ import annotations

import os
from typing import Any, Dict, Iterable

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(
    text: str, attributes: Iterable[str] = ("TOXICITY", "INSULT", "THREAT")
) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    requested = {attribute: {} for attribute in attributes}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": requested,
            "languages": ["en"],
            "doNotStore": True,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = {
        name: value["summaryScore"]["value"]
        for name, value in payload.get("attributeScores", {}).items()
    }
    flagged = any(score >= 0.7 for score in scores.values())
    return {
        "provider": "perspective_api",
        "scores": scores,
        "flagged": flagged,
        "raw": payload,
    }
