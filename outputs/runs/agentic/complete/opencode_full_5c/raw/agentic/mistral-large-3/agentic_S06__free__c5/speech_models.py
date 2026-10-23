from dataclasses import dataclass
from typing import Optional, List, Dict, Union


@dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclass
class AudioConfig:
    audio_encoding: str = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: Optional[VoiceSelection] = None
    audio_config: Optional[AudioConfig] = None


@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_config: Optional[Dict] = None


def normalize_voice_selection(voice: VoiceSelection) -> Dict:
    return {
        "language_code": voice.language_code,
        "name": voice.name,
        "ssml_gender": voice.ssml_gender,
    }


def normalize_audio_config(audio_config: AudioConfig) -> Dict:
    return {
        "audio_encoding": audio_config.audio_encoding,
        "speaking_rate": audio_config.speaking_rate,
        "pitch": audio_config.pitch,
        "volume_gain_db": audio_config.volume_gain_db,
    }
