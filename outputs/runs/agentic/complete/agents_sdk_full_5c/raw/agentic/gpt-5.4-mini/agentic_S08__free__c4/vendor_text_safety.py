from __future__ import annotations

from openai import OpenAI

MODERATION_MODEL = "omni-moderation-latest"


def vendor_text_safety(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model=MODERATION_MODEL, input=text)
    return result.model_dump()
