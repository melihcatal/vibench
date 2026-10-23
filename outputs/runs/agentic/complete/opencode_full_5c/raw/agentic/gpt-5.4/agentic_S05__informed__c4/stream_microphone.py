from __future__ import annotations

from typing import AsyncIterator, Callable

from speech_client import (
    async_request_iterable,
    build_recognizer_path,
    get_speech_client,
)
from speech_models import StreamingOptions, TranscriptChunk, collect_normalized_results


async def stream_microphone_audio(
    microphone_source: AsyncIterator[bytes],
    project_id: str,
    language_code: str = "en-US",
) -> AsyncIterator[TranscriptChunk]:
    client = get_speech_client()
    options = StreamingOptions(
        language_code=language_code, interim_results=True, model="latest_long"
    )
    recognizer = build_recognizer_path(project_id)
    responses = await client.streaming_recognize(
        requests=async_request_iterable(recognizer, microphone_source, options)
    )
    async for response in responses:
        for result in collect_normalized_results(response):
            yield result


async def stream_microphone_with_callback(
    microphone_source: AsyncIterator[bytes],
    project_id: str,
    on_transcript: Callable[[TranscriptChunk], None],
    language_code: str = "en-US",
) -> None:
    async for transcript in stream_microphone_audio(
        microphone_source, project_id, language_code=language_code
    ):
        on_transcript(transcript)
