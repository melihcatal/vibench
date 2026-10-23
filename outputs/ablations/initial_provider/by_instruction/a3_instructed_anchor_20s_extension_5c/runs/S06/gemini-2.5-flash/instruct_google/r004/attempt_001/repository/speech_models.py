from dataclasses import dataclass, field
from typing import Optional, Literal

@dataclass
class VoiceConfig:
    language_code: str = "en-US"
    name: Optional[str] = None
    ssml_gender: Optional[Literal["SSML_VOICE_GENDER_UNSPECIFIED", "MALE", "FEMALE", "NEUTRAL"]] = None

@dataclass
class AudioConfig:
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: VoiceConfig = field(default_factory=VoiceConfig)
    audio_config: AudioConfig = field(default_factory=AudioConfig)

@dataclass
class SynthesisResponse:
    audio_content: bytes
    
@dataclass
class ListVoicesResponse:
    voices: list
