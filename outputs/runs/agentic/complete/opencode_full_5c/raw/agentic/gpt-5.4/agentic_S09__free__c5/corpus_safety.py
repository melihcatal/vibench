from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def corpus_safety(texts: Sequence[str], model: str = "omni-moderation-latest") -> dict:
    client = OpenAI(
        api_key=__import__("os").getenv("OPENAI_API_KEY"),
        base_url=__import__("os").getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ),
    )
    response = client.moderations.create(model=model, input=list(texts))
    items = []
    for index, result in enumerate(response.results):
        items.append(
            {
                "index": index,
                "flagged": result.flagged,
                "categories": result.categories.model_dump(),
                "category_scores": result.category_scores.model_dump(),
            }
        )
    return {
        "provider": "openai",
        "model": model,
        "results": items,
    }
