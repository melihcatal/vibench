"""Define local request, response, and normalization helpers for Text-to-Speech."""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class TTSRequest:
    """Normalized TTS synthesis request."""
    text: str
    model_id: str
    voice_id: str
    output_format: str = "mp3_44100_128"
    stability: Optional[float] = None
    similarity_boost: Optional[float] = None
    style: Optional[float] = None
    use_speaker_boost: Optional[bool] = None

    def to_dict(self) -> dict:
        """Convert request to a dict suitable for API serialization."""
        data: dict[str, Any] = {
            "text": self.text,
            "model_id": self.model_id,
            "voice_id": self.voice_id,
            "output_format": self.output_format,
        }
        voice_settings: dict[str, Any] = {}
        if self.stability is not None:
            voice_settings["stability"] = self.stability
        if self.similarity_boost is not None:
            voice_settings["similarity_boost"] = self.similarity_boost
        if self.style is not None:
            voice_settings["style"] = self.style
        if self.use_speaker_boost is not None:
            voice_settings["use_speaker_boost"] = self.use_speaker_boost
        if voice_settings:
            data["voice_settings"] = voice_settings
        return data


@dataclass
class TTSResponse:
    """Normalized TTS synthesis response."""
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    model_id: str = ""
    voice_id: str = ""
    request_id: Optional[str] = None
    character_count: int = 0

    @property
    def file_extension(self) -> str:
        """Return file extension based on content type."""
        ext_map = {
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg",
            "audio/flac": ".flac",
        }
        return ext_map.get(self.content_type, ".mp3")

    @property
    def size_bytes(self) -> int:
        """Return the size of the audio payload."""
        return len(self.audio_bytes)


@dataclass
class VoiceInfo:
    """Normalized voice metadata."""
    voice_id: str
    name: str
    category: str = ""
    locale: str = ""
    gender: str = ""
    labels: dict[str, str] = field(default_factory=dict)
    preview_url: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Return a human-readable voice label."""
        parts = [self.name]
        if self.locale:
            parts.append(f"({self.locale})")
        return " ".join(parts)

    def matches_locale(self, target_locale: str) -> bool:
        """Check if this voice supports the target locale."""
        if not target_locale or not self.locale:
            return True
        return target_locale.lower() in self.locale.lower()


@dataclass
class VoiceSelectionResult:
    """Result of a voice selection or listing operation."""
    voices: list[VoiceInfo]
    selected_voice: Optional[VoiceInfo] = None
    total_count: int = 0

    def get_voice_by_id(self, voice_id: str) -> Optional[VoiceInfo]:
        """Look up a voice by its ID."""
        for v in self.voices:
            if v.voice_id == voice_id:
                return v
        return None

    def filter_by_locale(self, locale: str) -> "VoiceSelectionResult":
        """Return a new result filtered by locale match."""
        filtered = [v for v in self.voices if v.matches_locale(locale)]
        selected = filtered[0] if filtered else self.selected_voice
        return VoiceSelectionResult(
            voices=filtered,
            selected_voice=selected,
            total_count=len(filtered),
        )
