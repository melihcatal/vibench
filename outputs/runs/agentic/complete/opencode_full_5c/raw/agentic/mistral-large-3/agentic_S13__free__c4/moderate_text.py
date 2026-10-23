from typing import Dict
from safety_client import TextModerationClient
from safety_models import normalize_moderation_response, ModerationResult


def moderate_text(text: str) -> ModerationResult:
    """
    Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.
    Model: google/cloud-language-v1
    """
    client = TextModerationClient()
    response = client.moderate_text(text)
    return normalize_moderation_response(response)
