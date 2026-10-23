"""Local configuration and client helper utilities for Google Cloud Streaming Speech-to-Text."""

import os
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


def get_speech_client(
    credentials_path: Optional[str] = None,
) -> speech.SpeechClient:
    """Return a Google Cloud Speech client using application default credentials or explicit path."""
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return speech.SpeechClient()


def create_streaming_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: int = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "latest_long",
    alternative_language_codes: Optional[list] = None,
    max_alternatives: int = 1,
    profanity_filter: bool = False,
) -> speech.StreamingRecognitionConfig:
    """Build a StreamingRecognitionConfig for Google Cloud Speech-to-Text.

    Uses google.cloud.speech_v1p1beta1 SDK and the 'latest_long' model by default.
    """
    recognition_config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
        max_alternatives=max_alternatives,
        profanity_filter=profanity_filter,
    )
    if alternative_language_codes:
        recognition_config.alternative_language_codes.extend(
            alternative_language_codes
        )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )
    return streaming_config


def normalize_audio_chunk(
    raw_bytes: bytes,
    sample_rate: int = 16000,
) -> bytes:
    """Validate and normalize raw PCM audio bytes for Google Cloud Speech streaming.

    Expects 16-bit LINEAR16 PCM at the target sample rate.
    """
    if not raw_bytes:
        raise ValueError("Empty audio chunk")
    if len(raw_bytes) % 2 != 0:
        raise ValueError("Audio data must be 16-bit aligned")
    return raw_bytes


def build_streaming_request_generator(
    audio_generator,
    streaming_config: speech.StreamingRecognitionConfig,
):
    """Wrap an audio chunk generator into Google Cloud Speech streaming requests.

    Yields StreamingRecognizeRequest objects with config first, then audio content.
    """
    yield speech.StreamingRecognizeRequest(
        streaming_config=streaming_config
    )
    for chunk in audio_generator:
        normalized = normalize_audio_chunk(chunk)
        yield speech.StreamingRecognizeRequest(audio_content=normalized)
