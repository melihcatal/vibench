from __future__ import annotations

import asyncio
from typing import AsyncIterator, Optional

from speech_client import build_speech_client, request_stream_from_async_iterable
from speech_models import StreamingConfig, TranscriptEvent
from partial_results import iter_transcript_events


async def microphone_chunk_source(
    queue: "asyncio.Queue[Optional[bytes]]",
) -> AsyncIterator[bytes]:
    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        if chunk:
            yield chunk


async def stream_microphone_transcripts(
    microphone_queue: "asyncio.Queue[Optional[bytes]]",
    config: StreamingConfig | None = None,
) -> AsyncIterator[TranscriptEvent]:
    cfg = config or StreamingConfig(interim_results=True)
    client = build_speech_client()
    responses = await client.streaming_recognize(
        requests=request_stream_from_async_iterable(microphone_chunk_source(microphone_queue), cfg)
    )
    async for response in responses:
        for event in iter_transcript_events([response]):
            yield event
