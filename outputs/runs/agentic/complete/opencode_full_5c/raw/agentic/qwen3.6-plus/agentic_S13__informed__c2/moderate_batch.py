from safety_client import analyze_batch
from safety_models import BatchModerationRequest, BatchModerationResponse


def moderate_batch(texts: list[str]) -> BatchModerationResponse:
    request = BatchModerationRequest(texts=texts)
    return analyze_batch(request)
