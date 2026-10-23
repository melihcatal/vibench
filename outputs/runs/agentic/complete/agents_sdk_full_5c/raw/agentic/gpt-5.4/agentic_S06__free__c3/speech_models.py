from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    gender: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hertz: Optional[int] = None


@dataclass
class VoiceSummary:
    name: str
    language_codes: List[str] = field(default_factory=list)
    gender: Optional[str] = None
    natural_sample_rate_hertz: Optional[int] = None


@dataclass
class AudioResult:
    provider: str
    audio_bytes: bytes
    mime_type: str = "audio/mpeg"
    voice_name: Optional[str] = None
    request_id: Optional[str] = None


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    categories: List[str] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    provider: str
    vector: List[float]
    model: str


@dataclass
class TranscriptResult:
    provider: str
    transcript: str
    confidence: Optional[float] = None


def coalesce_text_input(text: Optional[str] = None, ssml: Optional[str] = None) -> Dict[str, str]:
    if text:
        return {"text": text}
    if ssml:
        return {"ssml": ssml}
    raise ValueError("Either text or ssml must be provided")


def decode_base64_audio(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_voice_record(voice: Dict[str, Any]) -> VoiceSummary:
    return VoiceSummary(
        name=voice.get("name", ""),
        language_codes=list(voice.get("languageCodes", []) or []),
        gender=voice.get("ssmlGender"),
        natural_sample_rate_hertz=voice.get("naturalSampleRateHertz"),
    )
