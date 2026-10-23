from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    audio_encoding: str = "MP3"
    sample_rate_hertz: Optional[int] = None

    def to_google_input(self) -> Dict[str, str]:
        if self.ssml:
            return {"ssml": self.ssml}
        return {"text": self.text or ""}

    def to_google_voice(self) -> Dict[str, str]:
        voice: Dict[str, str] = {"languageCode": self.language_code}
        if self.voice_name:
            voice["name"] = self.voice_name
        return voice

    def to_google_audio_config(self) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "audioEncoding": self.audio_encoding,
            "speakingRate": self.speaking_rate,
            "pitch": self.pitch,
        }
        if self.sample_rate_hertz:
            config["sampleRateHertz"] = self.sample_rate_hertz
        return config


@dataclass
class SynthesisResponse:
    audio_content: bytes
    provider: str = "google_cloud_text_to_speech"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    sample_rate_hertz: Optional[int] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_google_response(
        cls,
        response: Dict[str, Any],
        *,
        voice_name: Optional[str] = None,
        audio_encoding: str = "MP3",
        sample_rate_hertz: Optional[int] = None,
    ) -> "SynthesisResponse":
        encoded = response.get("audioContent", "")
        audio = base64.b64decode(encoded) if encoded else b""
        return cls(
            audio_content=audio,
            voice_name=voice_name,
            audio_encoding=audio_encoding,
            sample_rate_hertz=sample_rate_hertz,
            raw_response=response,
        )


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str]
    ssml_gender: Optional[str] = None
    natural_sample_rate_hertz: Optional[int] = None


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str = "google_cloud_translate"
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    blocked: bool
    categories: List[str]
    provider: str = "openai_moderations"
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str = "openai_embeddings"
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    transcript: str
    language: Optional[str] = None
    provider: str = "openai_audio_transcriptions"
    raw_response: Any = None
