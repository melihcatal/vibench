"""
profile_moderation.py
Moderate profile text before account activation.

Provider: Azure AI Content Safety (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import requests
from typing import Dict, List, Optional
from identity_models import normalize_email

# Azure AI Content Safety configuration
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_profile_text(
    display_name: str,
    bio: Optional[str] = None,
    custom_fields: Optional[Dict[str, str]] = None,
) -> Dict:
    """
    Moderates user profile text fields using Azure AI Content Safety.

    Analyzes text for hate, self-harm, sexual, and violence categories.

    Args:
        display_name: User's chosen display name.
        bio: Optional user biography text.
        custom_fields: Optional dict of additional text fields to moderate.

    Returns:
        Dict with moderation results including safety scores and a pass/fail verdict.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is not set.")
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is not set.")

    text_to_analyze = display_name
    if bio:
        text_to_analyze += " " + bio
    if custom_fields:
        for value in custom_fields.values():
            text_to_analyze += " " + value

    url = (
        f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
        f"?api-version={CONTENT_SAFETY_API_VERSION}"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text_to_analyze,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()

    category_scores = {}
    highest_severity = 0

    for item in result.get("categoriesAnalysis", []):
        category = item.get("category", "Unknown")
        severity = item.get("severity", 0)
        category_scores[category] = severity
        highest_severity = max(highest_severity, severity)

    is_safe = highest_severity <= 2  # Severity 0-2 considered acceptable
    verdict = "approved" if is_safe else "flagged"

    return {
        "verdict": verdict,
        "is_safe": is_safe,
        "highest_severity": highest_severity,
        "category_scores": category_scores,
        "moderated_text_preview": text_to_analyze[:100] + "..." if len(text_to_analyze) > 100 else text_to_analyze,
    }


def check_profile_activation_safe(
    display_name: str,
    bio: Optional[str] = None,
) -> bool:
    """
    Convenience function: returns True if profile text passes moderation.

    Args:
        display_name: User's display name.
        bio: Optional user biography.

    Returns:
        True if the profile is safe for activation.
    """
    result = moderate_profile_text(display_name=display_name, bio=bio)
    return result["is_safe"]


if __name__ == "__main__":
    result = moderate_profile_text(
        display_name="FriendlyUser42",
        bio="I love programming and open source software!",
    )
    print(f"Moderation verdict: {result['verdict']}")
    print(f"Category scores: {result['category_scores']}")
