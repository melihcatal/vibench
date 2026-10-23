import os

import requests

PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def is_safe_text(text: str) -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    for attr in scores.values():
        if attr.get("summaryScore", {}).get("value", 0.0) >= 0.5:
            return False
    return True
