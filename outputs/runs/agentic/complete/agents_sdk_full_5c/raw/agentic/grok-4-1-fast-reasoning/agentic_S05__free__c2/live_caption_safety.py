import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator, Dict, Any, Tuple

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def live_caption_safety(caption_generator) -> AsyncGenerator[Tuple[str, bool, Dict[str, bool]], None]:
    async for caption in caption_generator:
        response = await client.moderations.create(
            input=caption,
            model="text-moderation-latest"
        )
        result = response.results[0]
        is_safe = not result.flagged
        categories = {k: v for k, v in result.categories.items() if v}
        yield caption, is_safe, categories