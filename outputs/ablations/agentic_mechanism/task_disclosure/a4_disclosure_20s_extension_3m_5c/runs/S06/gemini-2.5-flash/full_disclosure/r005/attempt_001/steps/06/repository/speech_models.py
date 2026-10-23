
import dataclasses
from typing import Optional, Literal

@dataclasses.dataclass
class TTSRequest:
    """
    Represents a Text-to-Speech request.
    """
    text: str
    voice_id: str
    audio_format: Literal["mp3", "wav", "ogg", "flac"] = "mp3"
    speed: Optional[float] = None
    pitch: Optional[float] = None

@dataclasses.dataclass
class TTSResponse:
    """
    Represents a Text-to-Speech response.
    """
    audio_content: bytes
    audio_format: Literal["mp3", "wav", "ogg", "flac"]
    duration_seconds: float
    sample_rate_hz: int

def normalize_text(text: str) -> str:
    """
    Normalizes the input text for Text-to-Speech synthesis.
    This can include cleaning, expanding abbreviations, etc.
    For now, it's a simple passthrough.
    """
    # Example normalization: strip leading/trailing whitespace
    return text.strip()
