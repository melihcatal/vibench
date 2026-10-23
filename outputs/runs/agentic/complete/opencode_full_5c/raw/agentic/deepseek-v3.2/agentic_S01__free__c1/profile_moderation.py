import os
import requests
import json
from typing import Optional, Dict, Any
from identity_client import IdentityConfig
from identity_models import ModerationRequest, ModerationResponse


def moderate_profile_text(text: str, content_type: str = "profile") -> dict:
    """
    Moderate profile text before account activation using OpenAI Moderation API.
    """
    config = IdentityConfig()

    if not config.openai_api_key:
        raise ValueError("OpenAI API key not configured")

    try:
        # OpenAI Moderation API endpoint
        url = f"{config.openai_api_url}/moderations"

        # Prepare request headers
        headers = {
            "Authorization": f"Bearer {config.openai_api_key}",
            "Content-Type": "application/json",
        }

        # Prepare request payload
        payload = {"input": text, "model": "text-moderation-latest"}

        # Make API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        if "results" not in result or not result["results"]:
            raise Exception("No moderation results returned from OpenAI API")

        moderation_result = result["results"][0]

        # Check if content is flagged
        is_flagged = moderation_result["flagged"]
        categories = moderation_result["category_scores"]

        # Determine if content is approved (not flagged for hate, harassment, self-harm, sexual, violence)
        critical_categories = ["hate", "harassment", "self-harm", "sexual", "violence"]
        is_approved = not is_flagged

        # Get flagged categories with scores above threshold
        flagged_categories = {}
        threshold = 0.7  # 70% confidence threshold

        for category, score in categories.items():
            if score > threshold:
                flagged_categories[category] = score

        # If any critical categories are flagged, content is not approved
        for critical in critical_categories:
            if critical in flagged_categories:
                is_approved = False

        # Create sanitized version (basic sanitization)
        sanitized_text = text
        if not is_approved:
            # Replace potentially harmful content with placeholders
            # This is a simple example - in production, use more sophisticated sanitization
            sanitized_text = "[Content moderated - please revise]"

        return {
            "is_approved": is_approved,
            "flagged_categories": flagged_categories if flagged_categories else None,
            "moderation_score": moderation_result.get("score"),
            "sanitized_text": sanitized_text if not is_approved else None,
            "provider": "OpenAI Moderation API",
        }

    except requests.exceptions.RequestException as e:
        print(f"OpenAI API request error: {e}")
        raise
    except Exception as e:
        print(f"Moderation error: {e}")
        raise
