from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def moderate_transcript_text(segments: Iterable[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    text = "\n".join(segments)
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {
        "provider": "OpenAI",
        "model": "omni-moderation-latest",
        "flagged": item.flagged,
        "categories": item.categories.model_dump(),
        "category_scores": item.category_scores.model_dump(),
    }
