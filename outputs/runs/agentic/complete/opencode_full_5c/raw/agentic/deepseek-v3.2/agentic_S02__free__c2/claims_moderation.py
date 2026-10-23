import os
import requests
from typing import Dict, Any
from identity_models import ModerationRequest, ModerationResponse


def moderate_claims(request: ModerationRequest) -> ModerationResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"model": "text-moderation-latest", "input": request.text}

    response = requests.post(
        "https://api.openai.com/v1/moderations", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()
    moderation = result["results"][0]

    categories = moderation["categories"]
    category_scores = moderation["category_scores"]

    is_approved = not moderation["flagged"]

    return ModerationResponse(
        is_approved=is_approved,
        categories=category_scores,
        flagged=moderation["flagged"],
        provider="openai",
    )
