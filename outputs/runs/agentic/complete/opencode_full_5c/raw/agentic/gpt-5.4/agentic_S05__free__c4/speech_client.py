from __future__ import annotations

import os
from typing import AsyncIterable, Iterable

from google.cloud.speech_v1 import SpeechAsyncClient, SpeechClient
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)

from speech_models import StreamingAudioChunk, StreamingSessionConfig


def build_streaming_config(
    config: StreamingSessionConfig,
) -> StreamingRecognitionConfig:
    recognition_config = RecognitionConfig(
        encoding=getattr(RecognitionConfig.AudioEncoding, config.encoding),
        sample_rate_hertz=config.sample_rate_hz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
    )
    return StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=config.interim_results,
    )


def get_google_speech_client() -> SpeechClient:
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return SpeechClient()


def get_google_speech_async_client() -> SpeechAsyncClient:
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return SpeechAsyncClient()


def build_initial_request(config: StreamingSessionConfig) -> StreamingRecognizeRequest:
    return StreamingRecognizeRequest(streaming_config=build_streaming_config(config))


def request_iter_from_chunks(
    chunks: Iterable[StreamingAudioChunk], config: StreamingSessionConfig
):
    yield build_initial_request(config)
    for chunk in chunks:
        if chunk.content:
            yield StreamingRecognizeRequest(audio_content=chunk.content)


async def async_request_iter_from_chunks(
    chunks: AsyncIterable[StreamingAudioChunk], config: StreamingSessionConfig
):
    yield build_initial_request(config)
    async for chunk in chunks:
        if chunk.content:
            yield StreamingRecognizeRequest(audio_content=chunk.content)
