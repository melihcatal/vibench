from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None

@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None

@dataclass
class AudioConfig:
    audio_encoding: str = "mp3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None

@dataclass
class TextToSpeechConfig:
    api_key: str
    region: str
    voice: Optional[str] = None
    output_format: Optional[str] = "Audio16Khz32KBitRateMonoMp3" # Azure specific output format
