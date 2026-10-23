from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class TTSRequest:
    text: str
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0

    def to_openai_payload(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "input": self.text,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }


@dataclass
class TTSResponse:
    audio_bytes: bytes
    model: str
    voice: str
    format: str
    duration_estimate_ms: int = 0
    request_id: str = ""

    @classmethod
    def from_openai_response(
        cls, audio_bytes: bytes, request: TTSRequest
    ) -> TTSResponse:
        words = len(request.text.split())
        wpm = 150 / request.speed
        duration_ms = int((words / wpm) * 60 * 1000)
        return cls(
            audio_bytes=audio_bytes,
            model=request.model,
            voice=request.voice,
            format=request.response_format,
            duration_estimate_ms=duration_ms,
        )


@dataclass
class SSMLRequest:
    text: str
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0
    pitch: str = "default"
    volume: str = "default"

    def to_openai_payload(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "input": self.text,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }


@dataclass
class VoiceInfo:
    id: str
    locale: str
    gender: str
    accent: str
    sample_rate: int = 24000


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"
    preserve_formatting: bool = True


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    model: str = "gpt-4o-mini"


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class SafetyCheckResponse:
    is_safe: bool
    categories: dict[str, bool] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    model: str = "text-moderation-latest"


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    embedding: list[float]
    model: str
    text: str


@dataclass
class TranscriptionRequest:
    audio_bytes: bytes
    language: str | None = None
    response_format: str = "text"


@dataclass
class TranscriptionResponse:
    text: str
    language: str
    model: str = "whisper-1"


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def parse_ssml_tags(ssml: str) -> list[dict[str, Any]]:
    tags = []
    pattern = r"<(voice|prosody|break|emphasis|say-as)[^>]*>"
    for match in re.finditer(pattern, ssml):
        tag = match.group(1)
        attrs = {}
        attr_pattern = r'(\w+)="([^"]*)"'
        for attr_match in re.finditer(attr_pattern, match.group(0)):
            attrs[attr_match.group(1)] = attr_match.group(2)
        tags.append(
            {
                "tag": tag,
                "attributes": attrs,
                "start": match.start(),
                "end": match.end(),
            }
        )
    return tags


def strip_ssml_tags(ssml: str) -> str:
    plain = re.sub(r"<[^>]+>", "", ssml)
    plain = re.sub(r"&\w+;", "", plain)
    return normalize_text(plain)


def build_ssml_segments(
    text: str, voice: str, speed: float, pitch: str, volume: str
) -> str:
    prosody_attrs = []
    if speed != 1.0:
        prosody_attrs.append(f'rate="{speed}"')
    if pitch != "default":
        prosody_attrs.append(f'pitch="{pitch}"')
    if volume != "default":
        prosody_attrs.append(f'volume="{volume}"')
    prosody_open = f"<prosody {' '.join(prosody_attrs)}>" if prosody_attrs else ""
    prosody_close = "</prosody>" if prosody_attrs else ""
    return f'<speak><voice name="{voice}">{prosody_open}{text}{prosody_close}</voice></speak>'
