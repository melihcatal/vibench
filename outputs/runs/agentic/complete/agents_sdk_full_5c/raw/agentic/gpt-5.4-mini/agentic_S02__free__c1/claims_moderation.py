from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim_text(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    first = result.results[0]
    return {
        "flagged": first.flagged,
        "categories": dict(first.categories),
        "category_scores": dict(first.category_scores),
    }
