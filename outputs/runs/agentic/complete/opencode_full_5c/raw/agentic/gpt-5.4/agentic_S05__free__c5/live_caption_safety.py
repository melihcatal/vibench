from __future__ import annotations

import os

from openai import AsyncOpenAI

from speech_models import TranscriptChunk


async def check_live_caption_safety(chunk: TranscriptChunk) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI Moderations")
    client = AsyncOpenAI(api_key=api_key)
    result = await client.moderations.create(
        model="omni-moderation-latest", input=chunk.text
    )
    output = result.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": output.flagged,
        "categories": output.categories.model_dump()
        if hasattr(output.categories, "model_dump")
        else dict(output.categories),
        "text": chunk.text,
    }
