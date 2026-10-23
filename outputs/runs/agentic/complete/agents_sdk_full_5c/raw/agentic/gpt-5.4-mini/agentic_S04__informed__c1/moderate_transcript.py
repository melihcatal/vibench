import os

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(text: str, threshold: float = 0.7) -> dict[str, object]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    flagged = any(
        scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0) >= threshold
        for attr in ("TOXICITY", "INSULT", "PROFANITY")
    )
    return {"flagged": flagged, "scores": scores, "raw": data}
