from __future__ import annotations

import os

from openai import AsyncOpenAI


async def check_live_caption_safety(text: str) -> dict[str, object]:
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = await client.moderations.create(
        model="omni-moderation-latest", input=text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "provider": "OpenAI omni-moderation-latest",
    }
