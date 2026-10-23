import os
import requests
from typing import Dict, Any


def moderate_profile_text(text: str) -> Dict[str, Any]:
    """
    Moderate profile text before account activation using OpenAI's moderation API.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    url = "https://api.openai.com/v1/moderations"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": text, "model": "text-moderation-latest"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    moderation_result = result["results"][0]

    return {
        "flagged": moderation_result["flagged"],
        "categories": moderation_result["categories"],
        "category_scores": moderation_result["category_scores"],
        "safe": not moderation_result["flagged"],
    }


def check_profile_for_approval(profile_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Check multiple profile fields for moderation before account activation.
    """
    results = {}

    for field, text in profile_data.items():
        if text:
            results[field] = moderate_profile_text(text)

    overall_safe = all(result.get("safe", False) for result in results.values())

    return {
        "field_results": results,
        "overall_safe": overall_safe,
        "approval_recommended": overall_safe,
    }
