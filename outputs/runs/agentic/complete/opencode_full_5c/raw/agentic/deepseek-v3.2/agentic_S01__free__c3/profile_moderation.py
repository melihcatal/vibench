import os
import requests
from typing import List, Dict, Any
from identity_models import UserProfile


def moderate_profile_text(text: str) -> Dict[str, Any]:
    """Moderate profile text using OpenAI Moderation API."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": text, "model": "text-moderation-latest"}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()
    moderation_result = result["results"][0]

    return {
        "flagged": moderation_result["flagged"],
        "categories": moderation_result["categories"],
        "category_scores": moderation_result["category_scores"],
        "safe": not moderation_result["flagged"],
    }


def check_profile_for_activation(user_profile: UserProfile) -> Dict[str, Any]:
    """Check user profile for activation readiness using moderation."""
    checks = {"name_safe": True, "bio_safe": True, "overall_safe": True, "issues": []}

    # Check name if provided
    if user_profile.name:
        name_check = moderate_profile_text(user_profile.name)
        if name_check["flagged"]:
            checks["name_safe"] = False
            checks["overall_safe"] = False
            checks["issues"].append("Name contains inappropriate content")

    # Check metadata fields if available
    if user_profile.metadata:
        bio = user_profile.metadata.get("bio", "")
        if bio:
            bio_check = moderate_profile_text(bio)
            if bio_check["flagged"]:
                checks["bio_safe"] = False
                checks["overall_safe"] = False
                checks["issues"].append("Bio contains inappropriate content")

    return checks


def get_moderation_recommendations(moderation_result: Dict[str, Any]) -> List[str]:
    """Get recommendations based on moderation results."""
    recommendations = []

    if moderation_result["flagged"]:
        flagged_categories = [
            category
            for category, flagged in moderation_result["categories"].items()
            if flagged
        ]

        if flagged_categories:
            recommendations.append(
                f"Content flagged for: {', '.join(flagged_categories)}"
            )
            recommendations.append(
                "Please revise your profile text to remove inappropriate content."
            )

    return recommendations
