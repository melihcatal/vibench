from typing import List, Dict
from safety_client import TextModerationClient
from safety_models import normalize_moderation_response, ModerationResult


def moderate_batch(messages: List[str]) -> List[ModerationResult]:
    """
    Moderates a batch of user messages using Google Cloud Natural Language API.
    Model: google/cloud-language-v1
    """
    client = TextModerationClient()
    results = []

    for message in messages:
        response = client.moderate_text(message)
        results.append(normalize_moderation_response(response))

    return results
