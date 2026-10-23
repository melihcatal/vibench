from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


PROVIDER = "openai"
MODEL = "omni-moderation-latest"


def ocr_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.moderations.create(model=MODEL, input=text)
    moderation = result.results[0]
    return {
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump() if hasattr(moderation.categories, "model_dump") else dict(moderation.categories),
        "category_scores": moderation.category_scores.model_dump() if hasattr(moderation.category_scores, "model_dump") else dict(moderation.category_scores),
    }
