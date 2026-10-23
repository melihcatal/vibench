
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Standard-A"
    language_code: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    audio_encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000

@dataclass
class VoiceSelectionParams:
    language_code: str = "en-US"
    name: Optional[str] = None
    ssml_gender: Optional[str] = None # e.g., 'FEMALE', 'MALE', 'NEUTRAL'

@dataclass
class AudioSaveRequest:
    audio_content: bytes
    file_path: str
    file_name: str = "output.wav"
