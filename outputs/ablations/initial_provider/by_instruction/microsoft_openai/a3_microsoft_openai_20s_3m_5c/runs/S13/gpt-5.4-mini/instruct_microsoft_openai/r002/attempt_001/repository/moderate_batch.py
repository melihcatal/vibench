from typing import List

from safety_client import build_client, moderate_with_openai, get_response_item
from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationDecision, normalize_categories, normalize_text


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    client = build_client()
    texts = [normalize_text(message.text) for message in request.messages]
    response = moderate_with_openai(client, texts)
    decisions: List[ModerationDecision] = []
    for index, _message in enumerate(request.messages):
        item = get_response_item(response, index)
        categories = normalize_categories(getattr(item, "category_scores", {}))
        flagged = bool(getattr(item, "flagged", False))
        decisions.append(
            ModerationDecision(
                allowed=not flagged,
                flagged=flagged,
                categories=categories,
                category_applied_thresholds={},
                raw={"index": index},
            )
        )
    return BatchModerationResponse(decisions=decisions)
