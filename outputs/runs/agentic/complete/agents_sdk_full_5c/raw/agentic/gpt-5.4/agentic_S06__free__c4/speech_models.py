from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hertz: Optional[int] = None

    def to_google_payload(self) -> Dict[str, Any]:
        if not self.text and not self.ssml:
            raise ValueError("Either text or ssml must be provided")
        payload: Dict[str, Any] = {
            "voice": {
                "languageCode": self.language_code,
            },
            "audioConfig": {
                "audioEncoding": self.audio_encoding,
                "speakingRate": self.speaking_rate,
                "pitch": self.pitch,
            },
        }
        if self.voice:
            payload["voice"]["name"] = self.voice
        if self.sample_rate_hertz is not None:
            payload["audioConfig"]["sampleRateHertz"] = self.sample_rate_hertz
        if self.text is not None:
            payload["input"] = {"text": self.text}
        else:
            payload["input"] = {"ssml": self.ssml}
        return payload


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str] = field(default_factory=list)
    gender: Optional[str] = None
    natural_sample_rate_hertz: Optional[int] = None

    @classmethod
    def from_google_voice(cls, voice: Any) -> "VoiceOption":
        return cls(
            name=getattr(voice, "name", ""),
            language_codes=list(getattr(voice, "language_codes", []) or []),
            gender=str(getattr(voice, "ssml_gender", "")) or None,
            natural_sample_rate_hertz=getattr(voice, "natural_sample_rate_hertz", None),
        )


@dataclass
class AudioArtifact:
    content: bytes
    encoding: str
    voice_name: Optional[str] = None
    language_code: Optional[str] = None


@dataclass
class SafetyCheckResult:
    blocked: bool
    categories: Dict[str, float]
    provider: str = "OpenAI Moderations"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = "Google Cloud Translation"


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    provider: str = "OpenAI Embeddings"


@dataclass
class TranscriptResult:
    text: str
    language: Optional[str] = None
    provider: str = "OpenAI Audio Transcriptions"


def pick_voice_for_locale(voices: Iterable[VoiceOption], locale: str) -> Optional[VoiceOption]:
    locale_lower = locale.lower()
    exact = [v for v in voices if any(code.lower() == locale_lower for code in v.language_codes)]
    if exact:
        return sorted(exact, key=lambda v: v.name)[0]
    prefix = locale.split("-")[0].lower()
    partial = [v for v in voices if any(code.lower().startswith(prefix) for code in v.language_codes)]
    if partial:
        return sorted(partial, key=lambda v: v.name)[0]
    return None
