from __future__ import annotations

from typing import List

import requests

PROVIDER = "Perspective API"
ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_copy(text: str) -> List[str]:
    api_key = __import__("os").environ.get("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    resp = requests.post(f"{ENDPOINT}?key={api_key}", json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("attributeScores", {})
    flagged = []
    for name, score in data.items():
        if score.get("summaryScore", {}).get("value", 0) >= 0.5:
            flagged.append(name.lower())
    return flagged
