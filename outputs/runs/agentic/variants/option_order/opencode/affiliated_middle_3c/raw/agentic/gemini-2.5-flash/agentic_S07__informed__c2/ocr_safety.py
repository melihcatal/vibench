import os
import requests
from typing import Dict, Any
from document_models import SafetyCheckRequest, SafetyCheckResponse

# Perspective API details
# https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_ocr_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    payload = {
        "comment": {"text": request.text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],  # Assuming English for now, can be extended
    }
    params = {"key": PERSPECTIVE_API_KEY}

    response = requests.post(PERSPECTIVE_API_ENDPOINT, params=params, json=payload)
    response.raise_for_status()

    result = response.json()
    scores = {}
    if "attributeScores" in result:
        for attribute, data in result["attributeScores"].items():
            scores[attribute] = data["summaryScore"]["value"]

    return SafetyCheckResponse(scores=scores)
