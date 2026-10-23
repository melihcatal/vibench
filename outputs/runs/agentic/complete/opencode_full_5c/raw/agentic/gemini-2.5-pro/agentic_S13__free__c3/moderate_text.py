from safety_client import get_openai_client
from safety_models import ModerationRequest, ModerationResponse


def moderate_text(request: ModerationRequest) -> ModerationResponse:
    client = get_openai_client()
    response = client.moderations.create(input=request.text)
    result = response.results[0]
    return ModerationResponse(
        flagged=result.flagged,
        categories={
            name: value for name, value in result.categories.model_dump().items()
        },
        category_scores={
            name: value for name, value in result.category_scores.model_dump().items()
        },
    )
