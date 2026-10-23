from safety_client import AWSComprehendClient
from safety_models import BatchModerationRequest, BatchModerationResponse

def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    client = AWSComprehendClient()
    response = client.moderate_batch(request.texts)
    return response
