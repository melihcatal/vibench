import requests
import os
from model_models import SafetyCheckResult
from typing import Dict, Any


def check_platform_output_safety(text: str) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    # Example attributes, adjust as needed based on desired checks
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"],  # Specify language if known, or let API detect
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    result = response.json()
    return SafetyCheckResult(attribute_scores=result.get("attributeScores", {}))
