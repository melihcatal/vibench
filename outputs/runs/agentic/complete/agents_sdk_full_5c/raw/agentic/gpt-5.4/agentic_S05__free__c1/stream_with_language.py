from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from google.cloud.speech_v2.types import cloud_speech

from speech_client import build_streaming_config, create_speech_client, recognizer_name


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    *,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: str = "chirp_2",
):
    client = create_speech_client()
    config = build_streaming_config(
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
    )

    async def requests() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer_name(),
            streaming_config=config,
        )
        async for chunk in audio_source:
            if chunk:
                yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    return await client.streaming_recognize(requests=requests())
