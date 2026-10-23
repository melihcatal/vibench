from __future__ import annotations

from identity_client import get_openai_headers, post_json
from identity_models import ProfileModerationRequest


OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def profile_moderation(request: ProfileModerationRequest):
    response = post_json(
        OPENAI_MODERATIONS_URL,
        get_openai_headers(),
        {"model": OPENAI_MODERATION_MODEL, "input": request.profile_text},
    )
    result = response["results"][0]
    return {
        "flagged": result["flagged"],
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
