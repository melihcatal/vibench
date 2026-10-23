from __future__ import annotations

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claims_text(text: str) -> bool:
    client = OpenAI()
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    return not any(item.flagged for item in result.results)
