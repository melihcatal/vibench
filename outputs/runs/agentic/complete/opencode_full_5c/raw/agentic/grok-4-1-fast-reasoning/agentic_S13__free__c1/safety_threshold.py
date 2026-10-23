import os
import requests
from typing import Dict, Any, Optional


def safety_threshold(
    text: str, category_thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    if category_thresholds is None:
        category_thresholds = {
            "TOXICITY": 0.5,
            "SEVERE_TOXICITY": 0.5,
            "INSULT": 0.5,
            "PROFANITY": 0.5,
            "THREAT": 0.5,
            "SEXUALLY_EXPLICIT": 0.5,
            "IDENTITY_ATTACK": 0.5,
        }
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {k: {} for k in category_thresholds},
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    for attr, score_data in data["attributeScores"].items():
        scores[attr] = score_data["summaryScore"]["value"]
    flagged = any(
        scores.get(attr, 0.0) > thresh for attr, thresh in category_thresholds.items()
    )
    return {"safe": not flagged, "scores": scores}
