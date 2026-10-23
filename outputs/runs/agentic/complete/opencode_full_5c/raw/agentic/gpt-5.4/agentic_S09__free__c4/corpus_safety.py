from __future__ import annotations

import os
from collections.abc import Sequence

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def corpus_safety(texts: Sequence[str]) -> dict[str, object]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL, input=list(texts)
    )
    flagged = []
    for index, result in enumerate(response.results):
        categories = [
            name for name, enabled in result.categories.model_dump().items() if enabled
        ]
        flagged.append(
            {
                "index": index,
                "flagged": result.flagged,
                "categories": categories,
            }
        )
    return {
        "model": OPENAI_MODERATION_MODEL,
        "results": flagged,
        "safe": all(not item["flagged"] for item in flagged),
    }
