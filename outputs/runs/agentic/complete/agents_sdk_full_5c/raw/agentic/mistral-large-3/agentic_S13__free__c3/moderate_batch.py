from typing import List, Optional
from safety_models import BatchModerationRequest, ModerationDecision, SafetyCategory
from safety_client import GoogleContentSafetyClient


def moderate_batch(
    texts: List[str],
    categories: Optional[List[SafetyCategory]] = None,
    threshold: Optional[dict[SafetyCategory, float]] = None,
) -> List[ModerationDecision]:
    """
    Moderates a batch of user messages using Google Content Safety API.
    """
    client = GoogleContentSafetyClient()
    request: BatchModerationRequest = {
        "texts": texts,
        "categories": categories,
        "threshold": threshold,
    }
    return client.moderate_batch(request)