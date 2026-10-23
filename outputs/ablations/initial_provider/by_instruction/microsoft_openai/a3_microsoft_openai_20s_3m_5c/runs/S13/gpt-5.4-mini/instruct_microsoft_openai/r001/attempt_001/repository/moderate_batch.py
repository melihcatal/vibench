from safety_client import DEFAULT_MODERATION_MODEL, get_client, get_model, extract_categories, extract_category_scores
from safety_models import BatchModerationRequest, ModerationResult, normalize_messages, normalize_text


def moderate_batch(messages, model=None):
    request = BatchModerationRequest(messages=[normalize_text(m) for m in messages], model=model)
    client = get_client()
    moderation_model = get_model(request.model, DEFAULT_MODERATION_MODEL)
    response = client.moderations.create(model=moderation_model, input=request.messages)
    decisions = []
    for result in response.results:
        decisions.append(
            ModerationResult(
                allowed=not bool(result.flagged),
                categories=extract_categories(result),
                category_scores=extract_category_scores(result),
                raw=result.model_dump(),
            )
        )
    return {"decisions": decisions, "raw": response.model_dump()}
