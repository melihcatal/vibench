import os
import requests
from identity_models import ModerationRequest, ModerationResponse


def moderate_profile_text(
    text: str, content_type: str = "profile"
) -> ModerationResponse:
    """
    Moderate profile text before account activation using OpenAI Moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    url = "https://api.openai.com/v1/moderations"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"input": text, "model": "text-moderation-latest"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    result = data["results"][0]

    # Check if content is flagged
    flagged = result["flagged"]
    categories = result["category_scores"]

    # Get flagged categories with high confidence
    flagged_categories = []
    for category, score in categories.items():
        if score > 0.7:  # High confidence threshold
            flagged_categories.append(category)

    # Determine if text should be approved
    is_approved = not flagged

    return ModerationResponse(
        is_approved=is_approved,
        flagged_categories=flagged_categories,
        confidence=max(categories.values()) if categories else 0.0,
        moderated_text=text if is_approved else "[Content moderated]",
    )
