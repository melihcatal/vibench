from __future__ import annotations

import os
from typing import Optional

from google.cloud.speech_v2 import SpeechAsyncClient
from google.cloud.speech_v2.types import cloud_speech


GOOGLE_RECOGNIZER = os.getenv("GOOGLE_SPEECH_RECOGNIZER", "projects/demo/locations/global/recognizers/_")
GOOGLE_MODEL = os.getenv("GOOGLE_SPEECH_MODEL", "latest_short")
DEFAULT_LANGUAGE = os.getenv("GOOGLE_SPEECH_LANGUAGE", "en-US")


def create_speech_client(
    *,
    client: Optional[SpeechAsyncClient] = None,
) -> SpeechAsyncClient:
    return client or SpeechAsyncClient()


def build_streaming_config(
    *,
    language_code: str = DEFAULT_LANGUAGE,
    model: str = GOOGLE_MODEL,
    sample_rate_hz: int = 16000,
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
    )
    return cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            interim_results=interim_results,
        ),
    )


def recognizer_name(override: Optional[str] = None) -> str:
    return override or GOOGLE_RECOGNIZER
