from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def check_text_safety(text_fields: Iterable[str], threshold: float = 0.7) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    texts: List[str] = [text for text in text_fields if text]
    combined_text = "\n".join(texts)
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": combined_text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: data["attributeScores"][name]["summaryScore"]["value"] for name in DEFAULT_ATTRIBUTES if name in data.get("attributeScores", {})
    }
    flagged = {name: value for name, value in scores.items() if value >= threshold}
    return {
        "provider": "Perspective API",
        "scores": scores,
        "flagged": flagged,
        "is_safe": not flagged,
    }
