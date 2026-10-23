import os
import requests  # Provider-identifying signal
from typing import Dict
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(
    request: UnsafeContentCheckRequest,
) -> UnsafeContentCheckResponse:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {
        "key": PERSPECTIVE_API_KEY,
    }

    data = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": [request.language],
    }

    response = requests.post(PERSPECTIVE_API_URL, params=params, json=data)
    response.raise_for_status()
    result = response.json()

    attribute_scores: Dict[str, float] = {}
    is_unsafe = False

    for attribute, scores in result.get("attributeScores", {}).items():
        score = scores.get("summaryScore", {}).get("value", 0.0)
        attribute_scores[attribute] = score
        if score > 0.5:  # Threshold for considering content unsafe
            is_unsafe = True

    return UnsafeContentCheckResponse(is_unsafe=is_unsafe, categories=attribute_scores)
