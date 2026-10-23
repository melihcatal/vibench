from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from google.cloud.speech_v2.types import cloud_speech

from speech_client import build_streaming_config, create_speech_client, recognizer_name


async def stream_audio_chunks(
    chunk_source: AsyncIterable[bytes],
    *,
    language_code: str = "en-US",
    model: str = "latest_long",
):
    client = create_speech_client()
    streaming_config = build_streaming_config(
        language_code=language_code,
        model=model,
        interim_results=True,
    )

    async def request_iter() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer_name(),
            streaming_config=streaming_config,
        )
        async for chunk in chunk_source:
            if chunk:
                yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    return await client.streaming_recognize(requests=request_iter())
