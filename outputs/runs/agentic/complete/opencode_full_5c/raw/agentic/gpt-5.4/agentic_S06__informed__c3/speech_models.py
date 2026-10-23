from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SynthesisRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    rate: Optional[str] = None
    pitch: Optional[str] = None
    style: Optional[str] = None
    output_format: str = "audio-24khz-48kbitrate-mono-mp3"


@dataclass
class SynthesisResult:
    audio_bytes: bytes
    format: str
    duration_ms: Optional[int] = None
    request_id: Optional[str] = None
    provider: str = "azure-ai-speech"


@dataclass
class VoiceOption:
    short_name: str
    locale: str
    gender: Optional[str] = None
    style_list: List[str] = field(default_factory=list)
    sample_rate_hz: Optional[int] = None
    provider: str = "azure-ai-speech"


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str]
    target_language: str
    provider: str = "deepl"


@dataclass
class SafetyResult:
    flagged: bool
    category_scores: Dict[str, float]
    provider: str = "perspective-api"


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str = "openai"
    model: str = "text-embedding-3-large"


@dataclass
class TranscriptResult:
    transcript: str
    confidence: Optional[float] = None
    provider: str = "assemblyai"


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if not locale:
        return None
    cleaned = locale.replace("_", "-").strip()
    parts = cleaned.split("-")
    if len(parts) == 1:
        return parts[0].lower()
    return f"{parts[0].lower()}-{parts[1].upper()}"


def first_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray, dict)):
        return " ".join(str(item) for item in value)
    return str(value)
