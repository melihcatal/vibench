from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hertz: Optional[int] = None

    def validate(self) -> None:
        if not self.text and not self.ssml:
            raise ValueError("Either text or ssml must be provided.")
        if self.text and self.ssml:
            raise ValueError("Provide only one of text or ssml.")


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str] = field(default_factory=list)
    ssml_gender: Optional[str] = None
    natural_sample_rate_hertz: Optional[int] = None


@dataclass
class SynthesisResult:
    audio_bytes: bytes
    audio_encoding: str
    provider: str = "google-cloud-texttospeech"
    voice_name: Optional[str] = None
    language_code: Optional[str] = None
    sample_rate_hertz: Optional[int] = None


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    provider: str = "deepl"


@dataclass
class SafetyResult:
    safe: bool
    scores: Dict[str, float]
    flagged_categories: List[str]
    provider: str = "perspectiveapi"


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str = "openai"
    model: str = "text-embedding-3-small"


@dataclass
class TranscriptResult:
    transcript: str
    confidence: Optional[float] = None
    provider: str = "assemblyai"


GENDER_MAP = {
    "MALE": "MALE",
    "FEMALE": "FEMALE",
    "NEUTRAL": "NEUTRAL",
    "SSML_VOICE_GENDER_UNSPECIFIED": "NEUTRAL",
}


def normalize_voice(voice: Any) -> VoiceOption:
    gender_value = getattr(voice, "ssml_gender", None)
    gender_name = getattr(gender_value, "name", None) if gender_value is not None else None
    return VoiceOption(
        name=getattr(voice, "name", ""),
        language_codes=list(getattr(voice, "language_codes", []) or []),
        ssml_gender=GENDER_MAP.get(gender_name or str(gender_value), str(gender_value) if gender_value else None),
        natural_sample_rate_hertz=getattr(voice, "natural_sample_rate_hertz", None),
    )


def result_metadata(result: SynthesisResult) -> Dict[str, Any]:
    return {
        "provider": result.provider,
        "voice_name": result.voice_name,
        "language_code": result.language_code,
        "audio_encoding": result.audio_encoding,
        "sample_rate_hertz": result.sample_rate_hertz,
        "audio_size_bytes": len(result.audio_bytes),
    }
