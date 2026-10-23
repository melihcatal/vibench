from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import async_request_iter_from_chunks, get_google_speech_async_client
from speech_models import (
    StreamingAudioChunk,
    StreamingSessionConfig,
    StreamingTranscriptEvent,
    transcript_events_from_google,
)


async def stream_audio_chunks(
    source: AsyncIterable[bytes], config: StreamingSessionConfig | None = None
) -> AsyncIterator[StreamingTranscriptEvent]:
    session = config or StreamingSessionConfig()
    client = get_google_speech_async_client()

    async def wrapped_source() -> AsyncIterator[StreamingAudioChunk]:
        async for chunk in source:
            yield StreamingAudioChunk(content=chunk)

    responses = await client.streaming_recognize(
        requests=async_request_iter_from_chunks(wrapped_source(), session)
    )
    async for response in responses:
        for event in transcript_events_from_google(response):
            yield event
