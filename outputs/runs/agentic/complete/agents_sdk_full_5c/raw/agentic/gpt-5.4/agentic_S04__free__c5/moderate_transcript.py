from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"



def moderate_transcript(text: str) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Missing API key in {OPENAI_API_KEY_ENV}")
    client = OpenAI(api_key=api_key)
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    output = result.results[0]
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": output.flagged,
        "categories": output.categories.model_dump(),
        "category_scores": output.category_scores.model_dump(),
    }
