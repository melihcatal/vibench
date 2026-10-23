from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import build_speech_client, request_stream_from_async_iterable
from speech_models import StreamingConfig, TranscriptEvent
from partial_results import iter_transcript_events


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    config: StreamingConfig | None = None,
) -> AsyncIterator[TranscriptEvent]:
    cfg = config or StreamingConfig()
    client = build_speech_client()
    responses = await client.streaming_recognize(
        requests=request_stream_from_async_iterable(audio_source, cfg)
    )
    async for response in responses:
        for event in iter_transcript_events([response]):
            yield event
