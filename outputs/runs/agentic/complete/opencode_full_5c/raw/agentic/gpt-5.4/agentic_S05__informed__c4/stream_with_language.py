from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import (
    async_request_iterable,
    build_recognizer_path,
    get_speech_client,
)
from speech_models import StreamingOptions, TranscriptChunk, collect_normalized_results


async def stream_with_language_settings(
    audio_source: AsyncIterable[bytes],
    project_id: str,
    language_code: str,
    enable_punctuation: bool = True,
) -> AsyncIterator[TranscriptChunk]:
    client = get_speech_client()
    options = StreamingOptions(
        language_code=language_code,
        automatic_punctuation=enable_punctuation,
        interim_results=True,
        model="latest_long",
    )
    recognizer = build_recognizer_path(project_id)
    responses = await client.streaming_recognize(
        requests=async_request_iterable(recognizer, audio_source, options)
    )
    async for response in responses:
        for transcript in collect_normalized_results(response):
            yield transcript
