"""Local request, response, and normalization helpers for Text-to-Speech services."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TTSRequest:
    """Normalized text-to-speech request payload.

    This dataclass abstracts over provider-specific inputs
    and can be used with ElevenLabs, Azure Speech, Google Cloud TTS, etc.
    """

    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    language_code: Optional[str] = None
    speed: float = 1.0
    pitch: Optional[str] = None
    volume: Optional[str] = None
    output_format: str = "mp3"
    ssml: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def has_ssml(self) -> bool:
        """Return True if this request contains SSML markup."""
        return self.ssml is not None and len(self.ssml.strip()) > 0

    def get_text(self) -> str:
        """Return the text content, preferring SSML if available."""
        if self.has_ssml():
            return self.ssml  # type: ignore[return-value]
        return self.text

    def normalize_speed(self) -> str:
        """Convert speed multiplier to a percentage-based rate string.

        Returns a string like '+0%', '+25%', '-10%' suitable for
        SSML prosody rate attributes or provider APIs.
        """
        percentage = int((self.speed - 1.0) * 100)
        if percentage >= 0:
            return f"+{percentage}%"
        return f"{percentage}%"


@dataclass
class TTSResponse:
    """Normalized text-to-speech response containing audio and metadata.

    This dataclass abstracts over provider-specific outputs
    (ElevenLabs audio stream, Azure Speech audio_data, etc.)
    """

    audio_data: bytes
    format: str = "mp3"
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    sample_rate: Optional[int] = None
    channels: int = 1
    duration_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_empty(self) -> bool:
        """Return True if no audio data was produced."""
        return not self.audio_data or len(self.audio_data) == 0

    def byte_length(self) -> int:
        """Return the length of the audio data in bytes."""
        return len(self.audio_data)

    def to_file(self, path: str) -> str:
        """Write audio data to a local file.

        Args:
            path: Destination file path.

        Returns:
            The absolute path to the saved file.
        """
        import os

        with open(path, "wb") as f:
            f.write(self.audio_data)
        return os.path.abspath(path)


@dataclass
class VoiceInfo:
    """Normalized voice metadata from any TTS provider."""

    voice_id: str
    name: str
    language_code: str
    gender: str = "NEUTRAL"
    provider: str = "unknown"
    sample_rate_hz: Optional[int] = None
    model_family: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


def normalize_voice_gender(raw_gender: str) -> str:
    """Normalize various provider gender labels to a standard form.

    Maps provider-specific strings (e.g. 'Male', 'FEMALE', 1, 2)
    to 'MALE', 'FEMALE', or 'NEUTRAL'.
    """
    upper = raw_gender.strip().upper()
    if upper in ("MALE", "M", "1"):
        return "MALE"
    elif upper in ("FEMALE", "F", "2"):
        return "FEMALE"
    elif upper in ("NEUTRAL", "N", "0", "SSML_VOICE_GENDER_UNSPECIFIED", "UNSPECIFIED"):
        return "NEUTRAL"
    return "NEUTRAL"


def normalize_audio_format(format_hint: str) -> str:
    """Normalize provider-specific audio format strings to canonical forms.

    Args:
        format_hint: Raw format string from the provider.

    Returns:
        Canonical format string: 'mp3', 'wav', 'ogg', 'flac', or 'pcm'.
    """
    lower = format_hint.lower()
    if "mp3" in lower or "mpeg" in lower:
        return "mp3"
    elif "wav" in lower or "riff" in lower:
        return "wav"
    elif "ogg" in lower:
        return "ogg"
    elif "flac" in lower:
        return "flac"
    elif "pcm" in lower or "raw" in lower:
        return "pcm"
    return "mp3"
