from __future__ import annotations

from typing import Any, AsyncIterable, AsyncIterator

from speech_client import (
    aiter_audio_requests,
    build_initial_request,
    build_streaming_config,
    get_async_speech_client,
)
from speech_models import normalize_google_streaming_response


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes], language_code: str = "en-US"
) -> AsyncIterator[dict[str, Any]]:
    client = get_async_speech_client()
    config = build_streaming_config(language_code=language_code)

    async def request_iter() -> AsyncIterator:
        yield build_initial_request(config=config)
        async for request in aiter_audio_requests(audio_source):
            yield request

    responses = await client.streaming_recognize(requests=request_iter())
    async for response in responses:
        event = normalize_google_streaming_response(response)
        yield {
            "results": [
                {
                    "text": item.text,
                    "is_final": item.is_final,
                    "confidence": item.confidence,
                }
                for item in event.results
            ],
            "provider": "speech.googleapis.com",
        }
