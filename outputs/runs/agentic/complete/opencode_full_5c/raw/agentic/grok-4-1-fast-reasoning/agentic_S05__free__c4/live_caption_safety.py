import asyncio
from typing import AsyncGenerator
from openai import AsyncOpenAI
import os

async def safe_live_captions(captions: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    api_key = os.getenv(&quot;OPENAI_API_KEY&quot;)
    if not api_key:
        raise ValueError(&quot;OPENAI_API_KEY environment variable is required&quot;)
    client = AsyncOpenAI(api_key=api_key)
    async for caption in captions:
        if caption.strip():
            moderation = await client.moderations.create(
                input=caption,
                model=&quot;text-moderation-latest&quot;
            )
            if moderation.results[0].flagged:
                yield &quot;[FLAGGED]&quot;
            else:
                yield caption
