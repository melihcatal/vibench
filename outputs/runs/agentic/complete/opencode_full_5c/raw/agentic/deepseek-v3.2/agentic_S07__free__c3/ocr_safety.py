import os
from typing import List
import requests
from document_client import get_perspective_api_client
from document_models import (
    SafetyCheckRequest,
    SafetyCheckResponse,
    SafetyAttributeScore,
)


def ocr_safety(text: str, attributes: List[str] = None) -> SafetyCheckResponse:
    """
    Check extracted document text for unsafe content using Perspective API.
    """
    api_key = get_perspective_api_client()

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {attr: {} for attr in attributes},
    }

    response = requests.post(url, json=request_data)
    response.raise_for_status()
    result = response.json()

    scores = []
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score_data = attr_data.get("summaryScore", {})
        score = SafetyAttributeScore(
            attribute=attr_name,
            score=score_data.get("value", 0.0),
            summary_score=score_data.get("value", 0.0),
        )
        scores.append(score)

    return SafetyCheckResponse(
        scores=scores, provider="perspective_api", raw_response=result
    )
