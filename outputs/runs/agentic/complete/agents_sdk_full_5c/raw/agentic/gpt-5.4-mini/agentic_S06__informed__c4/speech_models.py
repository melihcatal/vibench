from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import texttospeech


@dataclass(frozen=True)
class TextRequest:
    text: str
    language_code: Optional[str] = None
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass(frozen=True)
class SsmlRequest:
    ssml: str
    language_code: Optional[str] = None
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass(frozen=True)
class SpeechResult:
    audio_content: bytes
    voice_name: Optional[str] = None
    language_code: Optional[str] = None
    audio_encoding: Optional[str] = None


def normalize_language_code(language_code: Optional[str], fallback: str = "en-US") -> str:
    value = (language_code or fallback).strip()
    return value or fallback


def build_voice_params(language_code: str, voice_name: Optional[str] = None) -> texttospeech.VoiceSelectionParams:
    kwargs: Dict[str, Any] = {"language_code": normalize_language_code(language_code)}
    if voice_name:
        kwargs["name"] = voice_name
    return texttospeech.VoiceSelectionParams(**kwargs)


def build_audio_config(encoding_name: str = "MP3", speaking_rate: float = 1.0, pitch: float = 0.0, volume_gain_db: float = 0.0) -> texttospeech.AudioConfig:
    return texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, encoding_name.upper(), texttospeech.AudioEncoding.MP3),
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )
