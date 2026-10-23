from __future__ import annotations

import asyncio
from typing import AsyncIterator

from stream_chunks import stream_audio_chunks
from speech_models import StreamingConfig, StreamingTranscriptEvent


async def microphone_chunk_source(queue: "asyncio.Queue[bytes | None]") -> AsyncIterator[bytes]:
    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk


async def stream_microphone_transcripts(
    microphone_queue: "asyncio.Queue[bytes | None]",
    language_code: str = "en-US",
) -> AsyncIterator[StreamingTranscriptEvent]:
    config = StreamingConfig(language_code=language_code, interim_results=True, punctuate=True)
    async for event in stream_audio_chunks(microphone_chunk_source(microphone_queue), config=config):
        yield event
