from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None

@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None
    natural_voice_profile: Optional[str] = None

@dataclass
class AudioConfig:
    audio_encoding: str = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None
    effects_profile_id: Optional[List[str]] = field(default_factory=list)

@dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelectionParams
    audio_config: AudioConfig

@dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes
    content_type: str = "audio/mpeg"

@dataclass
class Voice:
    name: str
    language_codes: List[str]
    ssml_gender: str
    natural_voice_profile: Optional[str] = None
    custom_voice_type: Optional[str] = None
    custom_voice_data_ready: Optional[bool] = None

@dataclass
class ListVoicesResponse:
    voices: List[Voice]
