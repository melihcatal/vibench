import os
import requests
from security_models import SafetyCheckRequest, SafetyCheckResponse


def check_payload_safety(text: str) -> SafetyCheckResponse:
    """Check decrypted text payloads for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return SafetyCheckResponse(
            is_safe=False,
            error="PERSPECTIVE_API_KEY not found in environment variables",
            provider="perspective_api",
        )

    try:
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
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()

        data = response.json()

        # Extract scores
        scores = {}
        categories = []
        is_safe = True

        for attribute_name, attribute_data in data.get("attributeScores", {}).items():
            score = attribute_data.get("summaryScore", {}).get("value", 0)
            scores[attribute_name.lower()] = score

            # Consider unsafe if any score > 0.7
            if score > 0.7:
                is_safe = False
                categories.append(attribute_name.lower())

        return SafetyCheckResponse(
            is_safe=is_safe,
            scores=scores,
            categories=categories if categories else None,
            provider="perspective_api",
        )
    except Exception as e:
        return SafetyCheckResponse(
            is_safe=False, error=str(e), provider="perspective_api"
        )
