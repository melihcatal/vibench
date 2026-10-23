from typing import Dict, Any
import os
import requests
from identity_models import ProfileModerationRequest, ProfileModerationResponse

# Perspective API configuration for text moderation
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def profile_moderation(request: ProfileModerationRequest) -> ProfileModerationResponse:
    """
    Moderates profile text using Perspective API for toxic content detection.
    """
    try:
        response = requests.post(
            PERSPECTIVE_API_URL,
            params={"key": PERSPECTIVE_API_KEY},
            json={
                "comment": {"text": request.text},
                "requestedAttributes": {"TOXICITY": {}},
            },
        )
        response.raise_for_status()
        toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]

        return ProfileModerationResponse(
            success=True,
            is_approved=toxicity_score < 0.7,
            toxicity_score=toxicity_score,
        )
    except Exception as e:
        return ProfileModerationResponse(success=False, error=str(e))
