from typing import NamedTuple, Optional

class VoiceConfig(NamedTuple):
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None # e.g., 'FEMALE', 'MALE', 'NEUTRAL'

class AudioConfig(NamedTuple):
    audio_encoding: str # e.g., 'LINEAR16', 'MP3', 'OGG_OPUS'
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None

class SynthesisRequest(NamedTuple):
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: VoiceConfig
    audio_config: AudioConfig
