from typing import List
from safety_client import get_openai_client
from safety_models import (
    BatchModerationRequest,
    BatchModerationResponse,
    ModerationResponse,
)


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    client = get_openai_client()
    response = client.moderations.create(input=request.texts)

    results: List[ModerationResponse] = []
    for res in response.results:
        results.append(
            ModerationResponse(
                flagged=res.flagged,
                categories={
                    name: value for name, value in res.categories.model_dump().items()
                },
                category_scores={
                    name: value
                    for name, value in res.category_scores.model_dump().items()
                },
            )
        )
    return BatchModerationResponse(results=results)
