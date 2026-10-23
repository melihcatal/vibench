import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, Dict, Any
import openai
from speech_models import Transcript


async def live_caption_safety(
    caption_stream: AsyncIterable[Transcript],
    api_key: str | None = None,
) -> AsyncGenerator[Dict[str, Any], None]:
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    client = openai.AsyncOpenAI(api_key=api_key)
    async for transcript in caption_stream:
        if transcript["is_final"]:
            text = transcript["text"]
            if text.strip():
                moderation = await client.moderations.create(
                    model="text-moderation-latest",
                    input=text,
                )
                result = moderation.results[0]
                flagged = any(result.categories.values())
                yield {
                    "text": text,
                    "safe": not flagged,
                    "categories": dict(result.categories),
                    "flagged_count": sum(result.categories.values()),
                }
