import os
import requests
import json


def check_content_safety(text: str, api_key: str = None) -> dict:
    """Check narration scripts for unsafe content using Perspective API."""
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
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

    response = requests.post(url, json=data)
    response.raise_for_status()

    result = response.json()

    scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        scores[attribute_name] = attribute_data.get("summaryScore", {}).get("value", 0)

    return {
        "scores": scores,
        "languages": result.get("languages", []),
        "detected_languages": result.get("detectedLanguages", []),
    }


def is_content_safe(text: str, threshold: float = 0.7, api_key: str = None) -> bool:
    """Check if content is safe based on toxicity threshold."""
    safety_result = check_content_safety(text, api_key)

    for attribute_name, score in safety_result["scores"].items():
        if score > threshold:
            return False

    return True
