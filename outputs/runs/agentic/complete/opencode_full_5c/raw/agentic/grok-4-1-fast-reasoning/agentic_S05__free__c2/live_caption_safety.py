import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator, Tuple


async def check_live_caption_safety(
    caption_gen: AsyncGenerator[str, None],
) -> AsyncGenerator[Tuple[str, bool], None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = AsyncOpenAI(api_key=api_key)

    async for caption in caption_gen:
        if not caption.strip():
            yield caption, True
            continue
        response = await client.moderations.create(
            model="text-moderation-latest", input=caption
        )
        flagged = response.results[0].flagged
        is_safe = not flagged
        yield caption, is_safe
