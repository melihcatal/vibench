from safety_client import DEFAULT_MODERATION_MODEL, get_client, get_model, extract_categories, extract_category_scores
from safety_models import ModerationRequest, ModerationResult, normalize_text


def moderate_text(text, model=None):
    request = ModerationRequest(text=normalize_text(text), model=model)
    client = get_client()
    moderation_model = get_model(request.model, DEFAULT_MODERATION_MODEL)
    response = client.moderations.create(model=moderation_model, input=request.text)
    result = response.results[0]
    return ModerationResult(
        allowed=not bool(result.flagged),
        categories=extract_categories(result),
        category_scores=extract_category_scores(result),
        raw=response.model_dump(),
    )
