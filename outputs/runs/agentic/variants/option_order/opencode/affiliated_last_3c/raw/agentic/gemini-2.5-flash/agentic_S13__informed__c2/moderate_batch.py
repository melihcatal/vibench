from typing import List
from safety_models import (
    BatchModerationRequest,
    BatchModerationResponse,
    TextModerationResponse,
    TextModerationRequest,
)
from moderate_text import moderate_text


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    results: List[TextModerationResponse] = []
    for text in request.texts:
        moderation_request = TextModerationRequest(text=text)
        response = moderate_text(moderation_request)
        results.append(response)
    return BatchModerationResponse(results=results)
