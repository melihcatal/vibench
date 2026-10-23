import os
from typing import List
from safety_client import PerspectiveClient
from safety_models import BatchModerationRequest, BatchModerationResponse, TextModerationResponse, TextModerationRequest

def moderate_batch(request: BatchModerationRequest, config=None) -> BatchModerationResponse:
    client = PerspectiveClient(api_key=config.get("api_key") if config else None)
    results: List[TextModerationResponse] = []
    for text_content in request.texts:
        text_request = TextModerationRequest(text=text_content)
        result = client.moderate_text(text_request)
        results.append(result)
    return BatchModerationResponse(results=results)
