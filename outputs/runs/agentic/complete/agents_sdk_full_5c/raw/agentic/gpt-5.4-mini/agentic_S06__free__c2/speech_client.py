from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import texttospeech


@dataclass(frozen=True)
class SpeechConfig:
    project_id: Optional[str] = None
    location: Optional[str] = None
    default_voice_name: Optional[str] = None
    default_language_code: str = "en-US"
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION") or "global",
        default_voice_name=os.getenv("TTS_DEFAULT_VOICE"),
        default_language_code=os.getenv("TTS_DEFAULT_LANGUAGE", "en-US"),
        audio_encoding=_parse_audio_encoding(os.getenv("TTS_AUDIO_ENCODING", "MP3")),
    )


def _parse_audio_encoding(value: str) -> texttospeech.AudioEncoding:
    normalized = value.strip().upper()
    return getattr(texttospeech.AudioEncoding, normalized, texttospeech.AudioEncoding.MP3)


@lru_cache(maxsize=1)
def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def build_voice(language_code: Optional[str] = None, voice_name: Optional[str] = None, ssml_gender: Optional[texttospeech.SsmlVoiceGender] = None) -> texttospeech.VoiceSelectionParams:
    return texttospeech.VoiceSelectionParams(
        language_code=language_code or load_speech_config().default_language_code,
        name=voice_name or load_speech_config().default_voice_name or "",
        ssml_gender=ssml_gender or texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
    )
