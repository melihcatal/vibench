from typing import List, Dict
from safety_client import TextModerator
from safety_models import normalize_response


def moderate_batch(messages: List[str]) -> List[Dict]:
    """
    Moderates a batch of user messages using Azure Content Safety.
    Model: 2024-02-15-preview
    """
    moderator = TextModerator()
    results = []
    for text in messages:
        response = moderator.moderate_text(text)
        results.append(normalize_response(response).dict())
    return results
