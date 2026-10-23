from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def moderate_claims_text(text: str) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    moderation = result.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump(),
        "category_scores": moderation.category_scores.model_dump(),
    }
