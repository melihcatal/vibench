from safety_client import get_openai_client, moderation_model, threshold_for
from safety_models import normalize_moderation_response


def safety_threshold(text: str, thresholds=None):
    client = get_openai_client()
    response = client.moderations.create(model=moderation_model(), input=text)
    result = normalize_moderation_response(response.model_dump())
    allowed = True
    for category, score in result.categories.items():
        if score >= threshold_for(category, thresholds):
            allowed = False
            break
    return {
        "allowed": allowed,
        "flagged": result.flagged,
        "categories": result.categories,
    }
