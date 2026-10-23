import os
import json
import requests


def check_message_safety(text):
    """Check message payload text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        url, params=params, data=json.dumps(payload), headers=headers
    )
    response.raise_for_status()

    result = response.json()

    attribute_scores = {}
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0)
        attribute_scores[attr_name] = score

    max_score = max(attribute_scores.values()) if attribute_scores else 0
    is_unsafe = max_score > 0.7

    unsafe_attributes = [
        attr for attr, score in attribute_scores.items() if score > 0.7
    ]

    return {
        "is_unsafe": is_unsafe,
        "max_score": max_score,
        "attribute_scores": attribute_scores,
        "unsafe_attributes": unsafe_attributes,
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
    }
