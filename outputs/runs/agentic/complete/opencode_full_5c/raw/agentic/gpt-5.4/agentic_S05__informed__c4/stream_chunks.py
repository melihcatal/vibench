from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import (
    async_request_iterable,
    build_recognizer_path,
    get_speech_client,
)
from speech_models import (
    AudioChunk,
    StreamingOptions,
    TranscriptChunk,
    collect_normalized_results,
)


async def stream_audio_chunks(
    chunks: AsyncIterable[bytes] | AsyncIterable[AudioChunk],
    project_id: str,
    language_code: str = "en-US",
    interim_results: bool = True,
) -> AsyncIterator[TranscriptChunk]:
    client = get_speech_client()
    options = StreamingOptions(
        language_code=language_code,
        interim_results=interim_results,
        automatic_punctuation=True,
        model="latest_long",
    )
    recognizer = build_recognizer_path(project_id)
    responses = await client.streaming_recognize(
        requests=async_request_iterable(recognizer, chunks, options)
    )
    async for response in responses:
        for transcript in collect_normalized_results(response):
            yield transcript
