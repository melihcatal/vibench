from safety_client import build_client, moderate_with_openai, moderation_thresholds, get_response_item
from safety_models import ModerationDecision, ModerationRequest, normalize_categories, normalize_text


def safety_threshold(request: ModerationRequest) -> ModerationDecision:
    client = build_client()
    thresholds = moderation_thresholds()
    text = normalize_text(request.text)
    response = moderate_with_openai(client, [text])
    item = get_response_item(response, 0)
    categories = normalize_categories(getattr(item, "category_scores", {}))
    flagged = False
    for category, score in categories.items():
        if score >= thresholds.get(category, 1.0):
            flagged = True
            break
    return ModerationDecision(
        allowed=not flagged,
        flagged=flagged,
        categories=categories,
        category_applied_thresholds=thresholds,
        raw={"thresholds": thresholds},
    )
