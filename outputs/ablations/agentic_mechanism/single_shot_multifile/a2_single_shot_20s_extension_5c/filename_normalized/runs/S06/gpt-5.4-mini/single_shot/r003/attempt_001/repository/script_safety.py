from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


MODEL = os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_script_safety(script: str) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    moderation = client.moderations.create(model=MODEL, input=script)
    result = moderation.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories), "category_scores": dict(result.category_scores)}
