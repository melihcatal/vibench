from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


OPENAI_PROVIDER = "openai"
OPENAI_MODEL = "omni-moderation-latest"


def visual_safety_text(labels: Iterable[str]) -> List[str]:
    values = [item.strip() for item in labels if item and item.strip()]
    if not values:
        return []
    client = OpenAI()
    response = client.moderations.create(model=OPENAI_MODEL, input="; ".join(values))
    result = response.results[0]
    flagged: List[str] = []
    categories = getattr(result, "categories", None)
    if categories:
        for name, is_flagged in categories.model_dump().items():
            if is_flagged:
                flagged.append(name)
    return flagged
