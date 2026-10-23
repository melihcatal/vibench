"""Local helper: request, response, and normalization helpers for Text-to-Speech."""

from dataclasses import dataclass, field
from typing import Optional
import base64
import json


@dataclass
class TTSRequest:
    """Normalized TTS synthesis request."""
    text: str
    voice_id: str = "default"
    model_id: str = ""
    speed: float = 1.0
    pitch: float = 0.0
    language_code: str = "en"
    output_format: str = "mp3"
    stability: Optional[float] = None
    similarity_boost: Optional[float] = None


@dataclass
class TTSResponse:
    """Normalized TTS synthesis response."""
    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    duration_ms: Optional[float] = None
    character_count: int = 0
    voice_name: str = ""
    model_used: str = ""

    @property
    def audio_b64(self) -> str:
        return base64.b64encode(self.audio_bytes).decode("utf-8")

    def to_dict(self) -> dict:
        return {
            "content_type": self.content_type,
            "duration_ms": self.duration_ms,
            "character_count": self.character_count,
            "voice_name": self.voice_name,
            "model_used": self.model_used,
            "audio_size_bytes": len(self.audio_bytes),
        }


@dataclass
class SSMLRequest:
    """Normalized SSML synthesis request."""
    ssml: str
    voice_name: str = "en-US-AriaNeural"
    output_format: str = "audio-24khz-48kbitrate-mono-mp3"
    language: str = "en-US"
    rate: str = "0%"
    pitch: str = "0Hz"
    volume: str = "default"


@dataclass
class VoiceInfo:
    """Normalized voice metadata."""
    voice_id: str
    name: str
    locale: str
    gender: str
    sample_rate: int = 24000
    preview_url: str = ""
    supported_formats: list = field(default_factory=list)
    custom_model_id: str = ""


@dataclass
class VoiceListResponse:
    """Normalized list of available voices."""
    voices: list = field(default_factory=list)
    total_count: int = 0

    def filter_by_locale(self, locale: str) -> "VoiceListResponse":
        filtered = [v for v in self.voices if v.locale.startswith(locale)]
        return VoiceListResponse(voices=filtered, total_count=len(filtered))


def normalize_audio_format(output_format: str) -> str:
    """Normalize audio format strings across providers."""
    mapping = {
        "mp3": "mp3",
        "mpeg": "mp3",
        "audio/mpeg": "mp3",
        "wav": "wav",
        "wave": "wav",
        "audio/wav": "wav",
        "ogg": "ogg",
        "opus": "opus",
        "pcm": "pcm",
        "flac": "flac",
    }
    return mapping.get(output_format.lower(), output_format)


def build_ssml(
    text: str,
    voice_name: str,
    language: str = "en-US",
    rate: str = "0%",
    pitch: str = "0Hz",
    volume: str = "default",
) -> str:
    """Build SSML markup string from parameters."""
    prosody_attrs = []
    if rate != "0%":
        prosody_attrs.append(f'rate="{rate}"')
    if pitch != "0Hz":
        prosody_attrs.append(f'pitch="{pitch}"')
    if volume != "default":
        prosody_attrs.append(f'volume="{volume}"')

    prosody_tag = ""
    if prosody_attrs:
        inner = " ".join(prosody_attrs)
        prosody_tag = f"<prosody {inner}>{text}</prosody>"
    else:
        prosody_tag = text

    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{language}">'
        f'<voice name="{voice_name}">'
        f"{prosody_tag}"
        f"</voice>"
        f"</speak>"
    )
    return ssml


def estimate_duration_ms(text: str, wpm: int = 150) -> float:
    """Estimate speech duration in milliseconds."""
    words = len(text.split())
    return (words / wpm) * 60 * 1000
