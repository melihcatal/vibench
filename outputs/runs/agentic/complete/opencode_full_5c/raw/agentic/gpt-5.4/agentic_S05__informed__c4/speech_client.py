from __future__ import annotations

import os
from typing import AsyncIterable, Iterable

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_models import AudioChunk, StreamingOptions


def get_speech_client() -> speech_v2.SpeechAsyncClient:
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is required")
    return speech_v2.SpeechAsyncClient()


def build_recognizer_path(project_id: str, recognizer_id: str = "_") -> str:
    return f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"


def build_streaming_config(
    options: StreamingOptions,
) -> cloud_speech.StreamingRecognitionConfig:
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[options.language_code],
        model=options.model,
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=options.automatic_punctuation,
        ),
    )
    return cloud_speech.StreamingRecognitionConfig(
        config=config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            interim_results=options.interim_results,
        ),
    )


def initial_request(
    recognizer: str, options: StreamingOptions
) -> cloud_speech.StreamingRecognizeRequest:
    return cloud_speech.StreamingRecognizeRequest(
        recognizer=recognizer,
        streaming_config=build_streaming_config(options),
    )


def audio_request(chunk: bytes) -> cloud_speech.StreamingRecognizeRequest:
    return cloud_speech.StreamingRecognizeRequest(audio=chunk)


def sync_request_iterable(
    recognizer: str,
    audio_chunks: Iterable[bytes],
    options: StreamingOptions,
) -> Iterable[cloud_speech.StreamingRecognizeRequest]:
    yield initial_request(recognizer, options)
    for chunk in audio_chunks:
        if chunk:
            yield audio_request(chunk)


async def async_request_iterable(
    recognizer: str,
    audio_chunks: AsyncIterable[bytes] | AsyncIterable[AudioChunk],
    options: StreamingOptions,
):
    yield initial_request(recognizer, options)
    async for chunk in audio_chunks:
        payload = chunk.data if isinstance(chunk, AudioChunk) else chunk
        if payload:
            yield audio_request(payload)
