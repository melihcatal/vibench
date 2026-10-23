from __future__ import annotations

from safety_client import moderate_text_request
from safety_models import ModerationRequest, moderation_result_to_dict


def score_text_for_safety(
    text: str,
    language: str | None = None,
    user_id: str | None = None,
    threshold: float = 0.7,
) -> dict:
    request = ModerationRequest(text=text, language=language, user_id=user_id)
    result = moderate_text_request(request, threshold=threshold)
    return moderation_result_to_dict(result)
