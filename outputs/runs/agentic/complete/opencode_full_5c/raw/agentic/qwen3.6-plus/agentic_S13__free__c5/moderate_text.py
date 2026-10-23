from safety_client import get_openai_client, MODERATION_MODEL
from safety_models import ModerationResult, parse_moderation_response


def moderate_text(text: str) -> ModerationResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=text,
    )
    raw = response.model_dump()
    return parse_moderation_response(text, raw)


def get_safety_score(text: str) -> float:
    result = moderate_text(text)
    return result.highest_score


def is_flagged(text: str) -> bool:
    result = moderate_text(text)
    return result.flagged


def get_flagged_categories(text: str) -> list[str]:
    result = moderate_text(text)
    return [c.category for c in result.categories if c.flagged]
