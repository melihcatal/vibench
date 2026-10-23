from __future__ import annotations

from collections.abc import AsyncGenerator, AsyncIterable

from speech_client import (
    build_streaming_request,
    create_speech_client,
    load_streaming_config,
    sync_audio_request_iter,
)
from speech_models import TranscriptEvent, normalize_google_streaming_response


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes], language_code: str = "en-US"
) -> AsyncGenerator[TranscriptEvent, None]:
    buffered_chunks = []
    async for chunk in audio_source:
        if chunk:
            buffered_chunks.append(chunk)
    client = create_speech_client()
    config = load_streaming_config(language_code=language_code, interim_results=True)
    streaming_config = build_streaming_request(config)
    responses = client.streaming_recognize(
        config=streaming_config, requests=sync_audio_request_iter(buffered_chunks)
    )
    for response in responses:
        for event in normalize_google_streaming_response(response):
            yield event
