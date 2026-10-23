from __future__ import annotations

import os
from typing import AsyncIterable, Iterable

from google.cloud import speech_v1 as speech

from speech_models import StreamingConfig


GOOGLE_SPEECH_MODEL = "latest_long"
GOOGLE_SPEECH_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def build_speech_client() -> speech.SpeechAsyncClient:
    if not os.getenv(GOOGLE_SPEECH_ENV):
        raise RuntimeError(f"Missing required environment variable: {GOOGLE_SPEECH_ENV}")
    return speech.SpeechAsyncClient()


def build_recognition_config(config: StreamingConfig) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hz,
        audio_channel_count=config.channels,
        language_code=config.language_code,
        model=GOOGLE_SPEECH_MODEL,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
    )


def build_streaming_config(config: StreamingConfig) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(config),
        interim_results=config.interim_results,
        single_utterance=False,
    )


def request_stream_from_iterable(
    chunks: Iterable[bytes],
    config: StreamingConfig,
) -> Iterable[speech.StreamingRecognizeRequest]:
    yield speech.StreamingRecognizeRequest(streaming_config=build_streaming_config(config))
    for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)


async def request_stream_from_async_iterable(
    chunks: AsyncIterable[bytes],
    config: StreamingConfig,
) -> AsyncIterable[speech.StreamingRecognizeRequest]:
    yield speech.StreamingRecognizeRequest(streaming_config=build_streaming_config(config))
    async for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)
