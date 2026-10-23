from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SpeechSynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hz: Optional[int] = None
    audio_encoding: str = "MP3"

    def is_ssml(self) -> bool:
        return bool(self.ssml)

    def to_google_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "voice": {
                "language_code": self.language_code,
            },
            "audio_config": {
                "audio_encoding": self.audio_encoding,
                "speaking_rate": self.speaking_rate,
                "pitch": self.pitch,
            },
        }
        if self.voice_name:
            payload["voice"]["name"] = self.voice_name
        if self.sample_rate_hz:
            payload["audio_config"]["sample_rate_hz"] = self.sample_rate_hz
        if self.ssml:
            payload["input"] = {"ssml": self.ssml}
        elif self.text is not None:
            payload["input"] = {"text": self.text}
        else:
            raise ValueError("Either text or ssml must be provided")
        return payload


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str] = field(default_factory=list)
    ssml_gender: Optional[str] = None
    natural_sample_rate_hertz: Optional[int] = None

    @classmethod
    def from_google_voice(cls, voice: Any) -> "VoiceOption":
        return cls(
            name=getattr(voice, "name", ""),
            language_codes=list(getattr(voice, "language_codes", []) or []),
            ssml_gender=str(getattr(voice, "ssml_gender", "")) if getattr(voice, "ssml_gender", None) is not None else None,
            natural_sample_rate_hertz=getattr(voice, "natural_sample_rate_hertz", None),
        )


@dataclass
class SynthesisResult:
    audio_bytes: bytes
    audio_encoding: str
    provider: str = "google-cloud-texttospeech"
    voice_name: Optional[str] = None
    sample_rate_hz: Optional[int] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language_code: Optional[str]
    target_language_code: str
    provider: str = "google-cloud-translate"


@dataclass
class SafetyCheckResult:
    blocked: bool
    categories: Dict[str, float]
    provider: str = "Google Cloud Natural Language"


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str = "text-embedding-004"
    provider: str = "Google Gemini"


@dataclass
class TranscriptResult:
    transcript: str
    confidence: Optional[float] = None
    provider: str = "google-cloud-speech"


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-").strip()


def filter_voices_for_locale(voices: Iterable[VoiceOption], locale: str) -> List[VoiceOption]:
    normalized = normalize_locale(locale)
    return [
        voice
        for voice in voices
        if any(code.lower() == normalized.lower() for code in voice.language_codes)
    ]
