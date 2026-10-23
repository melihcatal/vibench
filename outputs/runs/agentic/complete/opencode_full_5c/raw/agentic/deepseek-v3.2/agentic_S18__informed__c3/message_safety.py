import os
import json
from typing import Dict, Any, Optional
import requests


def check_message_safety(text: str) -> Dict[str, Any]:
    """Check message payload text for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

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

    params = {"key": api_key}

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        attribute_scores = result.get("attributeScores", {})

        safety_scores = {}
        for attribute, data in attribute_scores.items():
            score = data.get("summaryScore", {}).get("value", 0)
            safety_scores[attribute.lower()] = score

        max_score = max(safety_scores.values()) if safety_scores else 0
        is_unsafe = max_score > 0.7

        return {
            "is_unsafe": is_unsafe,
            "scores": safety_scores,
            "max_score": max_score,
            "provider": "Perspective API",
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "Perspective API",
            "api_endpoint": "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        }
