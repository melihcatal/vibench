from __future__ import annotations

import asyncio
import os
from typing import Any, AsyncIterable, AsyncIterator, Iterable

from google.cloud import speech

from speech_models import (
    StreamingSettings,
    build_streaming_config_payload,
    coerce_audio_chunk,
)


def get_speech_client() -> speech.SpeechAsyncClient:
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and not os.getenv(
        "GOOGLE_CLOUD_PROJECT"
    ):
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT for Google Cloud Speech"
        )
    return speech.SpeechAsyncClient()


def build_recognition_config(settings: StreamingSettings) -> speech.RecognitionConfig:
    payload = build_streaming_config_payload(settings)
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[payload["encoding"]],
        sample_rate_hertz=payload["sample_rate_hertz"],
        language_code=payload["language_code"],
        audio_channel_count=payload["audio_channel_count"],
        enable_automatic_punctuation=payload["enable_automatic_punctuation"],
        model=payload["model"],
    )


def build_streaming_config(
    settings: StreamingSettings,
) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(settings),
        interim_results=settings.interim_results,
        single_utterance=settings.single_utterance,
    )


async def streaming_request_iter(
    audio_chunks: AsyncIterable[bytes],
    settings: StreamingSettings,
) -> AsyncIterator[speech.StreamingRecognizeRequest]:
    yield speech.StreamingRecognizeRequest(
        streaming_config=build_streaming_config(settings)
    )
    async for chunk in audio_chunks:
        yield speech.StreamingRecognizeRequest(audio_content=coerce_audio_chunk(chunk))


async def collect_responses(
    audio_chunks: AsyncIterable[bytes],
    settings: StreamingSettings,
) -> Any:
    client = get_speech_client()
    requests = streaming_request_iter(audio_chunks, settings)
    return await client.streaming_recognize(requests=requests)


async def iterate_sync_chunks(chunks: Iterable[bytes]) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk
        await asyncio.sleep(0)
