from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from messaging_models import normalize_message_text


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_message_safety(payload: dict[str, Any]) -> dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = normalize_message_text(payload)
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    categories = {
        name: flagged
        for name, flagged in result.categories.model_dump().items()
        if flagged
    }
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "safe": not result.flagged,
        "flagged": result.flagged,
        "categories": categories,
        "text": text,
    }
