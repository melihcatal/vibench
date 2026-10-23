import os
from typing import Any

from openai import OpenAI

MODEL = os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_claims(text: str) -> dict[str, Any]:
    client = OpenAI()
    result = client.moderations.create(model=MODEL, input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": dict(item.categories), "category_scores": dict(item.category_scores)}
