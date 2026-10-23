from __future__ import annotations

import os

from openai import OpenAI


def moderate_transcript(text: str) -> dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    categories = {
        name: flagged
        for name, flagged in result.categories.model_dump().items()
        if flagged
    }
    return {
        "provider": "OpenAI",
        "model": "omni-moderation-latest",
        "flagged": result.flagged,
        "categories": categories,
    }
