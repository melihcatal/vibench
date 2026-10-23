from __future__ import annotations

import os
from typing import Optional

from google.cloud import speech_v1 as speech

from speech_models import StreamingRecognitionConfig


def get_google_speech_client() -> speech.SpeechAsyncClient:
    return speech.SpeechAsyncClient()


def get_google_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")


def build_streaming_config(
    config: StreamingRecognitionConfig,
) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, config.audio_encoding),
        sample_rate_hertz=config.sample_rate_hertz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=config.interim_results,
        single_utterance=False,
    )


def build_audio_request(chunk: bytes) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=chunk)


def build_config_request(
    config: StreamingRecognitionConfig,
) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(
        streaming_config=build_streaming_config(config)
    )
