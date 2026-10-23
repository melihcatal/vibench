import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = "omni-moderation-latest"


class ProfileModerationError(RuntimeError):
    pass


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def moderate_profile_text(profile_text: str, *, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    if not isinstance(profile_text, str) or not profile_text.strip():
        raise ValueError("profile_text must be a non-empty string")

    client = _client()
    response = client.moderations.create(model=model, input=profile_text)
    result = response.results[0]

    categories = getattr(result, "categories", None)
    category_scores = getattr(result, "category_scores", None)

    return {
        "provider": "openai",
        "model": model,
        "flagged": bool(result.flagged),
        "categories": categories.model_dump() if hasattr(categories, "model_dump") else dict(categories or {}),
        "category_scores": category_scores.model_dump() if hasattr(category_scores, "model_dump") else dict(category_scores or {}),
        "raw": response.model_dump() if hasattr(response, "model_dump") else response,
    }


def is_profile_approved(profile_text: str, *, model: str = DEFAULT_MODEL) -> bool:
    return not moderate_profile_text(profile_text, model=model)["flagged"]
