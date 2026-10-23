from __future__ import annotations

import os
from typing import AsyncIterable, Iterable

from google.cloud import speech_v1 as speech

from speech_models import StreamingConfig, pcm_chunk_to_google_request


def load_streaming_config(
    language_code: str = "en-US",
    sample_rate_hz: int = 16000,
    interim_results: bool = True,
    enable_automatic_punctuation: bool = True,
    model: str | None = "latest_long",
) -> StreamingConfig:
    return StreamingConfig(
        language_code=language_code,
        sample_rate_hz=sample_rate_hz,
        interim_results=interim_results,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
    )


def create_speech_client() -> speech.SpeechClient:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is required for Google Cloud Speech-to-Text"
        )
    return speech.SpeechClient()


def build_streaming_request(
    config: StreamingConfig,
) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
        model=config.model,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=config.interim_results,
        single_utterance=False,
    )


def sync_audio_request_iter(chunks: Iterable[bytes]):
    for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(**pcm_chunk_to_google_request(chunk))


async def async_audio_request_iter(chunks: AsyncIterable[bytes]):
    async for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(**pcm_chunk_to_google_request(chunk))
