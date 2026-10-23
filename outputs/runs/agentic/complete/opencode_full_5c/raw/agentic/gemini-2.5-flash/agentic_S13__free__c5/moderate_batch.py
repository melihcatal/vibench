from typing import List
from safety_models import BatchModerationRequest, BatchModerationResponse
from safety_client import batch_moderate_text_with_gcp


def moderate_batch(texts: List[str]) -> BatchModerationResponse:
    """Moderates a batch of user messages and returns per-message decisions using Google Cloud Natural Language API."""
    request = BatchModerationRequest(texts=texts)
    response = batch_moderate_text_with_gcp(request)
    return response
