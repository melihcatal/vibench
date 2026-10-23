from safety_client import build_client, moderate_with_openai, get_response_item
from safety_models import ModerationDecision, ModerationRequest, normalize_categories, normalize_text


def moderate_text(request: ModerationRequest) -> ModerationDecision:
    client = build_client()
    text = normalize_text(request.text)
    response = moderate_with_openai(client, [text])
    item = get_response_item(response, 0)
    categories = normalize_categories(getattr(item, "category_scores", {}))
    flagged = bool(getattr(item, "flagged", False))
    return ModerationDecision(
        allowed=not flagged,
        flagged=flagged,
        categories=categories,
        category_applied_thresholds={},
        raw={"id": getattr(response, "id", None), "result": getattr(item, "model_dump", lambda: {})()},
    )
