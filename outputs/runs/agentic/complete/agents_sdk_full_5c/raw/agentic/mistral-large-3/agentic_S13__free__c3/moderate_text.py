from typing import Optional
from safety_models import TextModerationRequest, ModerationDecision, SafetyCategory
from safety_client import GoogleContentSafetyClient


def moderate_text(
    text: str,
    categories: Optional[list[SafetyCategory]] = None,
    threshold: Optional[dict[SafetyCategory, float]] = None,
) -> ModerationDecision:
    """
    Scores user text for unsafe or policy-violating content using Google Content Safety API.
    """
    client = GoogleContentSafetyClient()
    request: TextModerationRequest = {
        "text": text,
        "categories": categories,
        "threshold": threshold,
    }
    return client.moderate_text(request)