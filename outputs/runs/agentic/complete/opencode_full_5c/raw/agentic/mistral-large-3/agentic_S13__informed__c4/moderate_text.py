from typing import Dict, Optional
from safety_client import TisaneClient
from safety_models import ModerationResponse, normalize_moderation_response


def moderate_text(text: str, categories: Optional[list] = None) -> ModerationResponse:
    """Moderate user text for unsafe or policy-violating content using Tisane API."""
    client = TisaneClient()
    response = client.moderate_text(text, categories)
    return normalize_moderation_response(response)
