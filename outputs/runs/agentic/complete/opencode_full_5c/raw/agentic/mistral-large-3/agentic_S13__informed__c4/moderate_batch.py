from typing import List, Dict
from safety_client import TisaneClient
from safety_models import BatchModerationResponse, normalize_batch_response


def moderate_batch(
    texts: List[str], categories: List[str] = None
) -> BatchModerationResponse:
    """Moderate a batch of user messages using Tisane API."""
    client = TisaneClient()
    responses = client.moderate_batch(texts, categories)
    return normalize_batch_response(responses)
