import os
import requests
from typing import Dict, List
from document_models import SafetyCheckResponse


def check_text_safety(text: str) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status()
    result = response.json()

    unsafe_categories = []
    confidence_scores = {}

    for attribute, data in result["attributeScores"].items():
        score = data["summaryScore"]["value"]
        confidence_scores[attribute] = score
        if score > 0.7:
            unsafe_categories.append(attribute)

    return SafetyCheckResponse(
        is_safe=len(unsafe_categories) == 0,
        unsafe_categories=unsafe_categories,
        confidence_scores=confidence_scores
    )