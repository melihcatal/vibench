import os
import requests
from typing import List
from model_models import SafetyRequest, SafetyResponse


def check_prompt_safety(text: str, check_type: str = "both") -> SafetyResponse:
    """Check prompts and generated text for unsafe content using OpenAI Moderation API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    url = "https://api.openai.com/v1/moderations"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": text, "model": "text-moderation-latest"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        moderation_result = result["results"][0]
        flagged = moderation_result["flagged"]
        categories = moderation_result["categories"]

        flagged_categories = []
        for category, is_flagged in categories.items():
            if is_flagged:
                flagged_categories.append(category)

        return SafetyResponse(
            is_safe=not flagged,
            flagged_categories=flagged_categories,
            confidence=moderation_result.get("category_scores", {}).get(
                "harassment/threatening", 0.0
            ),
            provider="openai",
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to check safety: {str(e)}")
