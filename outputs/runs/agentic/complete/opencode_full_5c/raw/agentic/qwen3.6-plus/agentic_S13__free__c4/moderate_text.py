from safety_client import call_moderation, OPENAI_MODERATION_MODEL
from safety_models import (
    ModerationRequest,
    ModerationResult,
    normalize_moderation_response,
    truncate_text,
)


def moderate_text(text, model=None):
    request = ModerationRequest(text=text)
    truncated = truncate_text(request.text)
    raw_response = call_moderation(truncated, model=model or OPENAI_MODERATION_MODEL)
    result = normalize_moderation_response(raw_response)
    return result


def moderate_text_with_details(text, model=None):
    request = ModerationRequest(text=text)
    truncated = truncate_text(request.text)
    raw_response = call_moderation(truncated, model=model or OPENAI_MODERATION_MODEL)
    result = normalize_moderation_response(raw_response)
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": [
            {"name": cs.name, "score": cs.score, "flagged": cs.flagged}
            for cs in result.category_scores
        ],
        "raw": result.raw_response,
    }
