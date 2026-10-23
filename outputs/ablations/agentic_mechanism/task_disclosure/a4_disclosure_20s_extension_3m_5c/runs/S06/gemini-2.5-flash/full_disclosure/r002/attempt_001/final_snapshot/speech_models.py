
import dataclasses
from typing import Optional, Literal

@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None

@dataclasses.dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None

@dataclasses.dataclass
class AudioConfig:
    audio_encoding: Literal["LINEAR16", "MP3", "OGG_OPUS"]
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None

@dataclasses.dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelectionParams
    audio_config: AudioConfig

@dataclasses.dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes

def normalize_text(text: str) -> str:
    """
    Normalizes text for speech synthesis by removing extra whitespace.
    """
    return " ".join(text.split())
