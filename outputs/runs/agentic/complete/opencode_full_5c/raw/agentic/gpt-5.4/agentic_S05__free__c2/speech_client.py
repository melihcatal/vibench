from __future__ import annotations

import os
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator

from google.cloud.speech_v2 import SpeechAsyncClient, SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_models import AudioChunk


DEFAULT_RECOGNIZER = os.getenv(
    "GOOGLE_CLOUD_SPEECH_RECOGNIZER", "projects/_/locations/global/recognizers/_"
)
DEFAULT_MODEL = os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "chirp_2")
DEFAULT_LANGUAGE = os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE", "en-US")
DEFAULT_SAMPLE_RATE = int(os.getenv("GOOGLE_CLOUD_SPEECH_SAMPLE_RATE_HZ", "16000"))


def get_speech_client() -> SpeechClient:
    return SpeechClient()


def get_async_speech_client() -> SpeechAsyncClient:
    return SpeechAsyncClient()


def build_streaming_config(
    *,
    language_code: str = DEFAULT_LANGUAGE,
    model: str = DEFAULT_MODEL,
    sample_rate_hz: int = DEFAULT_SAMPLE_RATE,
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
) -> cloud_speech.StreamingRecognitionConfig:
    recognition_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model=model,
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=enable_automatic_punctuation,
        ),
        explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hz,
            audio_channel_count=1,
        ),
    )
    return cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            interim_results=interim_results,
        ),
    )


def build_initial_request(
    *,
    recognizer: str = DEFAULT_RECOGNIZER,
    config: cloud_speech.StreamingRecognitionConfig,
) -> cloud_speech.StreamingRecognizeRequest:
    return cloud_speech.StreamingRecognizeRequest(
        recognizer=recognizer,
        streaming_config=config,
    )


def iter_audio_requests(
    chunks: Iterable[bytes | AudioChunk],
) -> Iterator[cloud_speech.StreamingRecognizeRequest]:
    for chunk in chunks:
        content = chunk.content if isinstance(chunk, AudioChunk) else chunk
        if content:
            yield cloud_speech.StreamingRecognizeRequest(audio=content)


async def aiter_audio_requests(
    chunks: AsyncIterable[bytes | AudioChunk],
) -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
    async for chunk in chunks:
        content = chunk.content if isinstance(chunk, AudioChunk) else chunk
        if content:
            yield cloud_speech.StreamingRecognizeRequest(audio=content)
