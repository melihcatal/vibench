from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


MODERATION_MODEL = "omni-moderation-latest"


def corpus_safety(texts: Sequence[str]) -> dict[str, object]:
    client = OpenAI()
    response = client.moderations.create(model=MODERATION_MODEL, input=list(texts))
    flagged_items = []
    for idx, result in enumerate(response.results):
        categories = {
            name: value
            for name, value in result.categories.__dict__.items()
            if value is True
        }
        flagged_items.append(
            {
                "index": idx,
                "flagged": result.flagged,
                "categories": categories,
            }
        )
    return {
        "model": MODERATION_MODEL,
        "results": flagged_items,
        "all_safe": all(not item["flagged"] for item in flagged_items),
    }
