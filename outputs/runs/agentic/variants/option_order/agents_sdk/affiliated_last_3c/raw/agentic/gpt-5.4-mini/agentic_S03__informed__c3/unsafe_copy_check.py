import os
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class UnsafeCopyResult:
    safe: bool
    score: float
    details: str


def check_unsafe_copy(text: str) -> UnsafeCopyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": api_key}
    response = requests.post(url, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return UnsafeCopyResult(safe=score < 0.5, score=score, details=str(data))
