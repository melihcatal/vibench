"""
Local request, response, and normalization helpers for Text-to-Speech.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Iterator


@dataclass
class TTSRequest:
    """Normalized text-to-speech request."""

    text: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True
    language_code: Optional[str] = None

    def to_elevenlabs_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for elevenlabs.generate call."""
        return {
            "text": self.text,
            "voice": self.voice_id,
            "model": self.model_id,
            "output_format": self.output_format,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
                "style": self.style,
                "use_speaker_boost": self.use_speaker_boost,
            },
        }


@dataclass
class SSMLRequest(TTSRequest):
    """Normalized SSML-based synthesis request."""

    ssml_text: str = ""
    apply_text_normalization: str = "auto"

    def __post_init__(self):
        if self.ssml_text:
            self.text = self.ssml_text

    def to_elevenlabs_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for elevenlabs.generate with SSML."""
        kwargs = super().to_elevenlabs_kwargs()
        kwargs["text"] = self.ssml_text
        kwargs["model"] = "eleven_multilingual_v2"
        return kwargs


@dataclass
class TTSResponse:
    """Normalized text-to-speech response."""

    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    duration_ms: Optional[float] = None
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    character_count: int = 0
    raw_response: Optional[Any] = None


@dataclass
class VoiceInfo:
    """Normalized voice metadata from ElevenLabs."""

    voice_id: str
    name: str
    category: str = ""
    description: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    locale: str = ""
    gender: str = ""
    preview_url: str = ""

    def matches_locale(self, target_locale: str) -> bool:
        """Check if this voice matches a target locale."""
        if not target_locale:
            return True
        target_lower = target_locale.lower()
        if self.locale.lower() == target_lower:
            return True
        if self.locale.lower().startswith(target_lower[:2]):
            return True
        for key, val in self.labels.items():
            if key.lower() in ("language", "locale", "accent"):
                if target_lower in val.lower() or val.lower() in target_lower:
                    return True
        return False


@dataclass
class VoiceList:
    """Collection of available voices."""

    voices: List[VoiceInfo] = field(default_factory=list)

    def filter_by_locale(self, locale: str) -> "VoiceList":
        """Return voices matching a locale."""
        return VoiceList(
            voices=[v for v in self.voices if v.matches_locale(locale)]
        )

    def get_by_id(self, voice_id: str) -> Optional[VoiceInfo]:
        """Get voice by ID."""
        for v in self.voices:
            if v.voice_id == voice_id:
                return v
        return None


def parse_elevenlabs_voice(raw_voice: Dict[str, Any]) -> VoiceInfo:
    """Parse an ElevenLabs voice dict into VoiceInfo."""
    labels = raw_voice.get("labels", {})
    return VoiceInfo(
        voice_id=raw_voice["voice_id"],
        name=raw_voice.get("name", ""),
        category=raw_voice.get("category", ""),
        description=raw_voice.get("description", ""),
        labels=labels,
        locale=labels.get("language", labels.get("accent", "")),
        gender=labels.get("gender", ""),
        preview_url=raw_voice.get("preview_url", ""),
    )


def parse_elevenlabs_voices_list(raw_data: Dict[str, Any]) -> VoiceList:
    """Parse ElevenLabs voices response into VoiceList."""
    voices_raw = raw_data.get("voices", [])
    return VoiceList(
        voices=[parse_elevenlabs_voice(v) for v in voices_raw]
    )
