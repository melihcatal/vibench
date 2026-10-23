from dataclasses import dataclass
from typing import Optional, Dict, Any
import base64


@dataclass
class SynthesisRequest:
    """Request model for text-to-speech synthesis."""

    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass
class SynthesisResponse:
    """Response model for text-to-speech synthesis."""

    audio_content: bytes
    audio_encoding: str
    request_id: Optional[str] = None

    def to_base64(self) -> str:
        """Convert audio content to base64 string."""
        return base64.b64encode(self.audio_content).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "audio_encoding": self.audio_encoding,
            "audio_size_bytes": len(self.audio_content),
            "audio_base64": self.to_base64(),
            "request_id": self.request_id,
        }


@dataclass
class VoiceInfo:
    """Voice information model."""

    name: str
    language_codes: list
    ssml_gender: str
    natural_sample_rate_hertz: int

    @classmethod
    def from_google_voice(cls, voice):
        """Create VoiceInfo from Google Cloud TTS Voice object."""
        from google.cloud import texttospeech

        return cls(
            name=voice.name,
            language_codes=list(voice.language_codes),
            ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
        )


def normalize_text_input(text: str, max_length: int = 5000) -> str:
    """Normalize text input for synthesis."""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    text = text.strip()

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def create_ssml_from_text(text: str, voice_params: Dict[str, Any] = None) -> str:
    """Create SSML from plain text with optional voice parameters."""
    if voice_params is None:
        voice_params = {}

    speaking_rate = voice_params.get("speaking_rate", 1.0)
    pitch = voice_params.get("pitch", 0.0)
    volume = voice_params.get("volume", "default")

    ssml = f"""<speak>
    <prosody rate="{speaking_rate}" pitch="{pitch}" volume="{volume}">
        {text}
    </prosody>
</speak>"""

    return ssml
