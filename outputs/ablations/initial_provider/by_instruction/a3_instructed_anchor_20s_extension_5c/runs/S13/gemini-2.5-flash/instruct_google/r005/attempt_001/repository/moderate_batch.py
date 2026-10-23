from typing import List
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_batch(texts: List[str]) -> List[ModerationResponse]:
    client = SafetyClient()
    requests = [ModerationRequest(text_content=text) for text in texts]
    responses = client.moderate_batch_text(requests)
    return responses
