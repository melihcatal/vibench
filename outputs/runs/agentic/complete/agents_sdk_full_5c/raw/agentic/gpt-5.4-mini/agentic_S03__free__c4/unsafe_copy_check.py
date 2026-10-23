"""Check localized copy for unsafe content using OpenAI moderation."""

from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


def check_unsafe_copy(text: str) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {
        "flagged": bool(item.flagged),
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
    }


__all__ = ["check_unsafe_copy"]
