# [HELPER] speech_models.py

from typing import NamedTuple, Optional


class SynthesisInput(NamedTuple):
    """Container for synthesis source; mirrors Google's protobuf equivalent.
    Supports plain text or SSML.
    """

    text: Optional[str] = None
    ssml: Optional[str] = None


class AudioConfig(NamedTuple):
    """Audio encoding settings; mirrors Google's protobuf AudioConfig.
    Minimal valid set for easy usage in helpers.
    """

    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


class VoiceSelectionParams(NamedTuple):
    """Voice identifier; mirrors Google's protobuf VoiceSelectionParams.
    Used as a simple dataclass wrapper for readability.
    """

    language_code: str = "en"
    name: str = "en-US"
