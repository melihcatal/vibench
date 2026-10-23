import asyncio
from typing import AsyncIterator
from speech_models import TranscriptChunk, TranscriptStream


async def handle_partial_results(stream: TranscriptStream) -> AsyncIterator[str]:
    buffer = []
    async for chunk in stream:
        partial = chunk["transcript"]
        if partial:
            buffer.append(partial)
        if chunk["is_final"]:
            final = " ".join(buffer).strip()
            if final:
                yield final
            buffer = []
