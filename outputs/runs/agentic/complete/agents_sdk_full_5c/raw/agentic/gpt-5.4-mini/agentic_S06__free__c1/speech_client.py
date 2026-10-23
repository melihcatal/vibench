from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import texttospeech

DEFAULT_LANGUAGE_CODE = os.getenv("TTS_DEFAULT_LANGUAGE_CODE", "en-US")
DEFAULT_VOICE_NAME = os.getenv("TTS_DEFAULT_VOICE_NAME", "en-US-Standard-C")
DEFAULT_SSML_GENDER = os.getenv("TTS_DEFAULT_SSML_GENDER", "NEUTRAL")

_GENDER_MAP = {
    "male": texttospeech.SsmlVoiceGender.MALE,
    "female": texttospeech.SsmlVoiceGender.FEMALE,
    "neutral": texttospeech.SsmlVoiceGender.NEUTRAL,
}


@dataclass(frozen=True)
class SpeechClientConfig:
    project_id: Optional[str] = None
    language_code: str = DEFAULT_LANGUAGE_CODE
    voice_name: str = DEFAULT_VOICE_NAME
    ssml_gender: str = DEFAULT_SSML_GENDER
    audio_encoding: str = "MP3"

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
            language_code=os.getenv("TTS_LANGUAGE_CODE", DEFAULT_LANGUAGE_CODE),
            voice_name=os.getenv("TTS_VOICE_NAME", DEFAULT_VOICE_NAME),
            ssml_gender=os.getenv("TTS_SSML_GENDER", DEFAULT_SSML_GENDER),
            audio_encoding=os.getenv("TTS_AUDIO_ENCODING", "MP3"),
        )


def build_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def gender_value(name: str):
    return _GENDER_MAP.get(name.lower(), texttospeech.SsmlVoiceGender.NEUTRAL)


def audio_encoding_value(name: str):
    mapping = {
        "mp3": texttospeech.AudioEncoding.MP3,
        "linear16": texttospeech.AudioEncoding.LINEAR16,
        "ogg_opus": texttospeech.AudioEncoding.OGG_OPUS,
        "mulaw": texttospeech.AudioEncoding.MULAW,
        "alaw": texttospeech.AudioEncoding.ALAW,
    }
    return mapping.get(name.lower(), texttospeech.AudioEncoding.MP3)
