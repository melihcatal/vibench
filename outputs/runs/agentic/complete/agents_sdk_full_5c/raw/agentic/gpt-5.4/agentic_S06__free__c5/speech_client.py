from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech


DEFAULT_TTS_MODEL_FAMILY = "Chirp 3 HD"
DEFAULT_GOOGLE_TTS_VOICE = os.getenv("GOOGLE_TTS_VOICE", "en-US-Chirp3-HD-Achernar")
DEFAULT_GOOGLE_LANGUAGE_CODE = os.getenv("GOOGLE_TTS_LANGUAGE_CODE", "en-US")
DEFAULT_AUDIO_ENCODING = os.getenv("GOOGLE_TTS_AUDIO_ENCODING", "MP3")


def get_google_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")


def get_texttospeech_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def build_voice_params(
    language_code: Optional[str] = None,
    voice_name: Optional[str] = None,
) -> texttospeech.VoiceSelectionParams:
    return texttospeech.VoiceSelectionParams(
        language_code=language_code or DEFAULT_GOOGLE_LANGUAGE_CODE,
        name=voice_name or DEFAULT_GOOGLE_TTS_VOICE,
    )


def build_audio_config(
    audio_encoding: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    sample_rate_hertz: Optional[int] = None,
) -> texttospeech.AudioConfig:
    encoding_name = (audio_encoding or DEFAULT_AUDIO_ENCODING).upper()
    encoding = getattr(texttospeech.AudioEncoding, encoding_name)
    config = texttospeech.AudioConfig(
        audio_encoding=encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    if sample_rate_hertz:
        config.sample_rate_hertz = sample_rate_hertz
    return config
