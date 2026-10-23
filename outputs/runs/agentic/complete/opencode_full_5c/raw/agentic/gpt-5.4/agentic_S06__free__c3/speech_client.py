from __future__ import annotations

import os
from typing import Any

from google.cloud import texttospeech

from speech_models import normalize_audio_encoding


def get_google_tts_client() -> texttospeech.TextToSpeechClient:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is required for Google Cloud Text-to-Speech"
        )
    return texttospeech.TextToSpeechClient()


def get_google_tts_model_config(
    audio_encoding: str, sample_rate_hertz: int | None = None
) -> dict[str, Any]:
    encoding_name = normalize_audio_encoding(audio_encoding)
    encoding = getattr(texttospeech.AudioEncoding, encoding_name)
    payload: dict[str, Any] = {"audio_encoding": encoding}
    if sample_rate_hertz:
        payload["sample_rate_hertz"] = sample_rate_hertz
    return payload


def build_voice_params(
    language_code: str, voice_name: str | None = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {"language_code": language_code}
    if voice_name:
        payload["name"] = voice_name
    return payload
