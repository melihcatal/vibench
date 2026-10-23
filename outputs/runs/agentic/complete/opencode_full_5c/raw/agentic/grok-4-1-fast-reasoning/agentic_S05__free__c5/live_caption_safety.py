import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from openai import AsyncOpenAI


async def check_live_caption_safety(
    caption_iter: AsyncIterable[str], threshold: float = 0.5
) -> AsyncGenerator[str, None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = AsyncOpenAI(api_key=api_key)
    async for caption in caption_iter:
        if not caption.strip():
            continue
        moderation = await client.moderations.create(input=caption)
        result = moderation.results[0]
        flagged = any(
            score > threshold for cat_score in result.category_scores.values()
        )
        if flagged:
            yield "[Content filtered for safety]"
        else:
            yield caption
