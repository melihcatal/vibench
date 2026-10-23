from typing import Dict
from safety_client import TextModerator
from safety_models import normalize_response


def moderate_text(text: str) -> Dict:
    """
    Scores user text for unsafe or policy-violating content using Azure Content Safety.
    Model: 2024-02-15-preview
    """
    moderator = TextModerator()
    response = moderator.moderate_text(text)
    return normalize_response(response).dict()
