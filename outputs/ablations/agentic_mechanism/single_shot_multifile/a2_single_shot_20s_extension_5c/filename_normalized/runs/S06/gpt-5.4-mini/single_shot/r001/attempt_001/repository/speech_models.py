from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextToSpeechRequest:
    text: str
    voice: str | None = None
    locale: str | None = None


@dataclass
class SsmlRequest:
    ssml: str
    voice: str | None = None
    locale: str | None = None
    pitch: str | None = None
    rate: str | None = None


@dataclass
class VoiceSelectionRequest:
    locale: str
    voice_name: str | None = None


@dataclass
class AudioResponse:
    audio: bytes
    content_type: str = 'audio/mpeg'


@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    ssml_gender: str | None = None


def normalize_locale(locale: str | None) -> str:
    return locale or 'en-US'


def normalize_text_request(request: TextToSpeechRequest) -> TextToSpeechRequest:
    request.text = ' '.join(request.text.split())
    return request


def normalize_ssml_request(request: SsmlRequest) -> SsmlRequest:
    request.ssml = request.ssml.strip()
    return request
