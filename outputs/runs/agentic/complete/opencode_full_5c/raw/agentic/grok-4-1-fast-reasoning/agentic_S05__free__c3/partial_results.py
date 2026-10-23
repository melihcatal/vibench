import asyncio
from typing import AsyncGenerator
from speech_models import TranscriptChunk


async def partial_results(
    stream: AsyncGenerator[TranscriptChunk, None],
) -> AsyncGenerator[str, None]:
    buffer = ""
    async for chunk in stream:
        buffer += chunk.text
        status = "FINAL" if chunk.is_final else "PARTIAL"
        yield f"[{status}] {buffer} (confidence: {chunk.confidence or 0:.2f})"
        if chunk.is_final:
            buffer = ""
