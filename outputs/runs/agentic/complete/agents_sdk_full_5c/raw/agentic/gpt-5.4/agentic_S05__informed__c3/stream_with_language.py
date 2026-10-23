from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import build_speech_client, request_stream_from_async_iterable
from speech_models import StreamingConfig, TranscriptEvent
from partial_results import iter_transcript_events


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language_code: str,
    enable_automatic_punctuation: bool = True,
) -> AsyncIterator[TranscriptEvent]:
    config = StreamingConfig(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
    )
    client = build_speech_client()
    responses = await client.streaming_recognize(
        requests=request_stream_from_async_iterable(audio_source, config)
    )
    async for response in responses:
        for event in iter_transcript_events([response]):
            yield event
