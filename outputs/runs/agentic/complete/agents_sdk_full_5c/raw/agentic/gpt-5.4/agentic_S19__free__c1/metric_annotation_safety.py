from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODEL = "omni-moderation-latest"


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(model=OPENAI_MODEL, input=text)
    output = result.results[0]
    return {
        "model": OPENAI_MODEL,
        "flagged": output.flagged,
        "categories": output.categories.model_dump() if hasattr(output.categories, "model_dump") else dict(output.categories),
        "category_scores": output.category_scores.model_dump() if hasattr(output.category_scores, "model_dump") else dict(output.category_scores),
    }
