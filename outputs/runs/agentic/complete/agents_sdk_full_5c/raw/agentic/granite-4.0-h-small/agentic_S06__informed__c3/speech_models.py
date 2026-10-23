from enum import Enum, auto
from typing import TypedDict

class VoiceInfo(TypedDict):
    """Subset of Azure Speech voice metadata."""
    name: str
    locale: str
    gender: str  # e.g., `Male`, `Female`, `Neutral"
    language: str

class OutputFormat(Enum):
    """Supported audio output formats."""
    WAV = auto()  # PCM 16‑bit mono
    MP3 = auto()  # not implemented in this snippet
    OGG = auto()  # not implemented in this snippet

def parse_voice_info(voice: dict) -> VoiceInfo:
    """Convert raw Azure SDK voice dict to our typedef."""
    return VoiceInfo(
        name=voice["Name"],
        locale=voice["Locale"],
        gender=voice["Gender"],  # Azure uses `Male`, `Female`, `Neutral`
        language=voice["Language"],
    )
