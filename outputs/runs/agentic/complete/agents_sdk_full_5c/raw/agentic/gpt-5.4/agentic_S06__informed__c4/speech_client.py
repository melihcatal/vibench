from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech

from speech_models import normalize_audio_encoding


_PROVIDER = "google-cloud-texttospeech"
_ENCODING_MAP = {
    "mp3": texttospeech.AudioEncoding.MP3,
    "linear16": texttospeech.AudioEncoding.LINEAR16,
    "ogg_opus": texttospeech.AudioEncoding.OGG_OPUS,
}


def get_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def get_provider_name() -> str:
    return _PROVIDER


def get_google_credentials_path() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def to_google_audio_encoding(audio_encoding: Optional[str]) -> texttospeech.AudioEncoding:
    normalized = normalize_audio_encoding(audio_encoding)
    if normalized not in _ENCODING_MAP:
        raise ValueError(f"Unsupported audio encoding for Google Cloud Text-to-Speech: {normalized}")
    return _ENCODING_MAP[normalized]


def build_voice_params(language_code: str, voice_name: Optional[str] = None) -> texttospeech.VoiceSelectionParams:
    kwargs = {"language_code": language_code}
    if voice_name:
        kwargs["name"] = voice_name
    return texttospeech.VoiceSelectionParams(**kwargs)


def build_audio_config(
    audio_encoding: Optional[str] = None,
    sample_rate_hz: Optional[int] = None,
    speaking_rate: Optional[float] = None,
    pitch: Optional[float] = None,
) -> texttospeech.AudioConfig:
    kwargs = {"audio_encoding": to_google_audio_encoding(audio_encoding)}
    if sample_rate_hz:
        kwargs["sample_rate_hertz"] = sample_rate_hz
    if speaking_rate is not None:
        kwargs["speaking_rate"] = speaking_rate
    if pitch is not None:
        kwargs["pitch"] = pitch
    return texttospeech.AudioConfig(**kwargs)
