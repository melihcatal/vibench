import os
from typing import Optional
import requests
from model_models import SafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def check_prompt_safety(
    text: str,
    api_key: Optional[str] = None,
    attributes: Optional[list] = None,
    threshold: float = 0.7,
) -> SafetyResult:
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    attrs = attributes or DEFAULT_ATTRIBUTES
    requested_attributes = {attr: {} for attr in attrs}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en"],
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": key},
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    scores = {}
    flagged = []
    for attr_name, attr_data in data.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged.append(attr_name)

    return SafetyResult(
        is_safe=len(flagged) == 0,
        scores=scores,
        flagged_attributes=flagged,
    )
