from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import (
    build_audio_request,
    build_config_request,
    get_google_speech_client,
)
from speech_models import (
    StreamingRecognitionConfig,
    StreamingTranscriptEvent,
    normalize_async_audio_source,
    normalize_google_streaming_response,
)


async def stream_audio_chunks(
    source: AsyncIterable[bytes],
    config: StreamingRecognitionConfig,
) -> AsyncIterator[StreamingTranscriptEvent]:
    async def request_iter():
        yield build_config_request(config)
        async for chunk in normalize_async_audio_source(source):
            yield build_audio_request(chunk.audio)

    client = get_google_speech_client()
    responses = await client.streaming_recognize(requests=request_iter())
    async for response in responses:
        for event in normalize_google_streaming_response(response):
            yield event
