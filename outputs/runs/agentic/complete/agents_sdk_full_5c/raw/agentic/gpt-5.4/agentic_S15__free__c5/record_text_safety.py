from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def record_text_safety(text_fields: Iterable[str]) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs: List[str] = [value for value in text_fields if value]
    moderation = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=inputs)
    flagged = any(result.flagged for result in moderation.results)
    categories = [result.categories.model_dump() for result in moderation.results]
    return {
        "flagged": flagged,
        "model": OPENAI_MODERATION_MODEL,
        "results": categories,
    }
