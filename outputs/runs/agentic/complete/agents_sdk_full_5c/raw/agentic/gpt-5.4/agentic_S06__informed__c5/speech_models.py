from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TTSRequest:
    text: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    language_code: Optional[str] = None
    stability: Optional[float] = None
    similarity_boost: Optional[float] = None
    style: Optional[float] = None
    use_speaker_boost: Optional[bool] = None


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"


@dataclass
class VoiceOption:
    voice_id: str
    name: str
    labels: Dict[str, Any] = field(default_factory=dict)
    preview_url: Optional[str] = None


@dataclass
class AudioArtifact:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    provider: str = "ElevenLabs"
    model_id: Optional[str] = None
    voice_id: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = "DeepL"


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    provider: str
    text: str
    confidence: Optional[float] = None
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_audio_content_type(output_format: str) -> str:
    lowered = output_format.lower()
    if lowered.startswith("mp3"):
        return "audio/mpeg"
    if lowered.startswith("pcm"):
        return "audio/wav"
    if lowered.startswith("ulaw"):
        return "audio/basic"
    return "application/octet-stream"


def coalesce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)
