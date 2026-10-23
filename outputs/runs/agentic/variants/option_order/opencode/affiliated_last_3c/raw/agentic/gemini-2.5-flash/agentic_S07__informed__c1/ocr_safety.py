import os
import requests
from document_models import SafetyCheckRequest, SafetyCheckResponse


def check_content_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Checks extracted document text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}

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
        "languages": ["en"],
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    unsafe_categories = []
    scores = {}

    attribute_scores = result.get("attributeScores", {})
    for attr, details in attribute_scores.items():
        summary_score = details.get("summaryScore", {}).get("value")
        if summary_score is not None:
            scores[attr.lower()] = summary_score
            if summary_score > 0.5:  # Arbitrary threshold for "unsafe"
                unsafe_categories.append(attr.lower())

    return SafetyCheckResponse(unsafe_categories=unsafe_categories, scores=scores)
