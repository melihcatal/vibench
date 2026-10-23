from safety_client import (
    get_openai_client,
    build_moderation_payload,
    parse_moderation_response,
    MODERATION_MODEL,
)
from safety_models import ModerationRequest, ModerationResult, normalize_category_scores


def moderate_text(
    text: str, request_id: str | None = None, model: str = MODERATION_MODEL
) -> ModerationResult:
    client = get_openai_client()
    payload = build_moderation_payload(text, model=model)
    response = client.moderations.create(**payload)
    parsed = parse_moderation_response(response)
    category_scores = normalize_category_scores(
        parsed["categories"], parsed["category_scores"]
    )
    return ModerationResult(
        text=text,
        flagged=parsed["flagged"],
        category_scores=category_scores,
        request_id=request_id,
    )
