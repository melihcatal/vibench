from __future__ import annotations

import os
from typing import Any, AsyncIterable, Iterable

from google.cloud import speech_v1 as speech

from speech_models import (
    StreamSettings,
    StreamingAudioChunk,
    build_google_streaming_config,
)


def load_stream_settings(
    *,
    sample_rate_hz: int = 16000,
    language_code: str = "en-US",
    interim_results: bool = True,
    enable_automatic_punctuation: bool = True,
) -> StreamSettings:
    return StreamSettings(
        sample_rate_hz=sample_rate_hz,
        language_code=language_code,
        interim_results=interim_results,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )


def create_speech_client() -> speech.SpeechClient:
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return speech.SpeechClient()


def make_streaming_config(
    settings: StreamSettings,
) -> speech.StreamingRecognitionConfig:
    payload = build_google_streaming_config(settings)
    recognition_config = speech.RecognitionConfig(**payload["config"])
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=payload["interim_results"],
    )


def request_iterator(
    chunks: Iterable[StreamingAudioChunk],
) -> Iterable[speech.StreamingRecognizeRequest]:
    for chunk in chunks:
        yield speech.StreamingRecognizeRequest(audio_content=chunk.content)


async def async_request_iterator(
    chunks: AsyncIterable[StreamingAudioChunk],
) -> AsyncIterable[speech.StreamingRecognizeRequest]:
    async for chunk in chunks:
        yield speech.StreamingRecognizeRequest(audio_content=chunk.content)


def start_streaming_recognition(
    client: speech.SpeechClient,
    settings: StreamSettings,
    chunks: Iterable[StreamingAudioChunk],
) -> Any:
    config = make_streaming_config(settings)
    return client.streaming_recognize(config=config, requests=request_iterator(chunks))
