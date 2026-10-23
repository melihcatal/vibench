from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


_MODERATION_MODEL = os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_claim_text(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(model=_MODERATION_MODEL, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
        "model": _MODERATION_MODEL,
    }
