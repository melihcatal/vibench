import asyncio
import os
from typing import AsyncGenerator
from openai import AsyncOpenAI
from speech_models import TranscriptChunk


async def live_caption_safety(
    caption_stream: AsyncGenerator[TranscriptChunk, None],
) -> AsyncGenerator[TranscriptChunk, None]:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    async for chunk in caption_stream:
        if not chunk.text.strip():
            yield chunk
            continue
        moderation = await client.moderations.create(
            model="text-moderation-latest", input=chunk.text
        )
        if not moderation.results[0].flagged:
            yield chunk
