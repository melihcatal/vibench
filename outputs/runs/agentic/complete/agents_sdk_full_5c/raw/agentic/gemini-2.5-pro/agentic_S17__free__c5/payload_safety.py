import os
from typing import Dict, Any

from security_client import get_perspective_api_client
from security_models import ContentSafetyRequest, ContentSafetyResponse


def check_content_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    """
    Analyzes text for toxicity and other attributes using Google's Perspective API.

    Args:
        request: A ContentSafetyRequest object with the text to analyze.

    Returns:
        A ContentSafetyResponse indicating if the content is safe and attribute scores.
    """
    client = get_perspective_api_client()

    analyze_request = {
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

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores: Dict[str, Any] = {
            attr: data["summaryScore"]["value"]
            for attr, data in response["attributeScores"].items()
        }

        # Define "unsafe" as any category scoring above a threshold, e.g., 0.7
        threshold = 0.7
        is_safe = all(score < threshold for score in scores.values())

        return ContentSafetyResponse(is_safe=is_safe, scores=scores)

    except Exception as e:
        print(f"Perspective API request failed: {e}")
        # Default to safe in case of API error to avoid blocking content unnecessarily
        return ContentSafetyResponse(is_safe=True, scores={})
