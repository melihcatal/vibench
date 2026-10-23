from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from speech_client import (
    aiter_audio_requests,
    build_initial_request,
    build_streaming_config,
    get_async_speech_client,
)
from speech_models import normalize_google_streaming_response


async def start_streaming_recognizer(
    audio_source: AsyncIterable[bytes],
    *,
    language_code: str,
    enable_automatic_punctuation: bool = True,
) -> AsyncIterator[dict[str, object]]:
    client = get_async_speech_client()
    config = build_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    async def request_iter() -> AsyncIterator:
        yield build_initial_request(config=config)
        async for request in aiter_audio_requests(audio_source):
            yield request

    responses = await client.streaming_recognize(requests=request_iter())
    async for response in responses:
        event = normalize_google_streaming_response(response)
        for result in event.results:
            yield {
                "text": result.text,
                "language_code": language_code,
                "is_final": result.is_final,
                "automatic_punctuation": enable_automatic_punctuation,
                "model": "chirp_2",
            }
