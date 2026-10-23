from typing import List
from safety_models import BatchModerationResponse
from moderate_text import moderate_text


def moderate_batch(texts: List[str]) -> BatchModerationResponse:
    results = []
    for text in texts:
        moderation_result = moderate_text(text)
        results.append(moderation_result)

    return BatchModerationResponse(results=results)
