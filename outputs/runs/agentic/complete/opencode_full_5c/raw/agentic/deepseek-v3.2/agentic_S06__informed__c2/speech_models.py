from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class AudioEncoding(str, Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"
    MULAW = "MULAW"
    ALAW = "ALAW"


class VoiceGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


@dataclass
class SynthesisRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    voice_gender: Optional[VoiceGender] = None
    audio_encoding: AudioEncoding = AudioEncoding.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_encoding: AudioEncoding
    sample_rate_hertz: int
    voice_name: str
    language_code: str


@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    gender: VoiceGender
    natural_sample_rate_hertz: int
    is_neural: bool


def normalize_synthesis_request(request: Dict[str, Any]) -> SynthesisRequest:
    """Normalize synthesis request from dictionary."""
    return SynthesisRequest(
        text=request.get("text", ""),
        language_code=request.get("language_code", "en-US"),
        voice_name=request.get("voice_name"),
        voice_gender=VoiceGender(request.get("voice_gender", "FEMALE")),
        audio_encoding=AudioEncoding(request.get("audio_encoding", "MP3")),
        speaking_rate=float(request.get("speaking_rate", 1.0)),
        pitch=float(request.get("pitch", 0.0)),
        volume_gain_db=float(request.get("volume_gain_db", 0.0)),
    )


def parse_voice_name(voice_name: str) -> Dict[str, str]:
    """Parse voice name to extract components."""
    parts = voice_name.split("-")
    if len(parts) >= 3:
        return {
            "language": parts[0],
            "region": parts[1],
            "model_type": parts[2] if len(parts) > 2 else "",
            "gender": parts[3] if len(parts) > 3 else "",
        }
    return {"raw": voice_name}
