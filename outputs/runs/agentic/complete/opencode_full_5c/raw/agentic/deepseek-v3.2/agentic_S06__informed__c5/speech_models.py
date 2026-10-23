from dataclasses import dataclass
from typing import Optional, Dict, Any
import base64


@dataclass
class SynthesisRequest:
    """Define local request helper for Text-to-Speech."""

    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_id: Optional[str] = None
    language_code: str = "en-US"
    audio_format: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0

    def to_google_input(self):
        """Convert to Google Cloud TTS input format."""
        if self.ssml:
            return {"ssml": self.ssml}
        else:
            return {"text": self.text}

    def to_google_voice(self):
        """Convert to Google Cloud TTS voice format."""
        return {
            "language_code": self.language_code,
            "name": self.voice_id or "en-US-Neural2-J",
            "ssml_gender": "FEMALE",
        }

    def to_google_audio_config(self):
        """Convert to Google Cloud TTS audio config format."""
        return {
            "audio_encoding": self.audio_format,
            "speaking_rate": self.speaking_rate,
            "pitch": self.pitch,
            "volume_gain_db": self.volume_gain_db,
        }


@dataclass
class SynthesisResponse:
    """Define local response helper for Text-to-Speech."""

    audio_content: bytes
    request: SynthesisRequest
    voice_used: str
    language_code: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "audio_content_b64": base64.b64encode(self.audio_content).decode("utf-8"),
            "voice_used": self.voice_used,
            "language_code": self.language_code,
            "audio_size_bytes": len(self.audio_content),
        }

    def save_to_file(self, filepath: str) -> str:
        """Save audio content to file."""
        with open(filepath, "wb") as f:
            f.write(self.audio_content)
        return filepath


def normalize_text_input(text: str, max_length: int = 5000) -> str:
    """
    Normalize text input for synthesis.
    """
    if not text:
        raise ValueError("Text cannot be empty")

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text.strip()


def create_ssml(
    text: str,
    voice_id: str = None,
    prosody_rate: str = "medium",
    prosody_pitch: str = "medium",
) -> str:
    """
    Create SSML from plain text with prosody controls.
    """
    ssml = f"""<speak>
    <prosody rate="{prosody_rate}" pitch="{prosody_pitch}">
        {text}
    </prosody>
</speak>"""
    return ssml
