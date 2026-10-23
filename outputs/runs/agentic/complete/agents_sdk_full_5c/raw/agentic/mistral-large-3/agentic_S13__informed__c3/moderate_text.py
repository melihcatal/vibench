import os
from typing import Dict
from safety_client import get_watsonx_client
from safety_models import TextModerationResponse


def moderate_text(text: str) -> TextModerationResponse:
    """
    Moderate a single text using WatsonX.ai guardrails.
    Returns normalized moderation response.
    """
    client = get_watsonx_client()
    raw_response = client.analyze_text(text)
    return TextModerationResponse.from_watsonx(raw_response)