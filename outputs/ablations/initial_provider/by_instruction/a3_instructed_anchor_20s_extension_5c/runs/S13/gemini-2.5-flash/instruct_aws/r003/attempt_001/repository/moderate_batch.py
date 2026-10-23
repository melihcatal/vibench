from typing import List
from safety_models import BatchModerationRequest, BatchModerationResponse, TextModerationResponse
from moderate_text import moderate_text

def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    results: List[TextModerationResponse] = []
    for text in request.texts:
        individual_request = TextModerationRequest(text=text)
        result = moderate_text(individual_request)
        results.append(result)
    return BatchModerationResponse(results=results)
