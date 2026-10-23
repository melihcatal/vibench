from dataclasses import dataclass
from typing import Optional, List, Dict, Any
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
    gender: VoiceGender = VoiceGender.NEUTRAL
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
    language_codes: List[str]
    gender: VoiceGender
    natural_sample_rate_hertz: int


def normalize_synthesis_request(request: Dict[str, Any]) -> SynthesisRequest:
    """Normalize a synthesis request dictionary to a SynthesisRequest object."""
    return SynthesisRequest(
        text=request.get("text", ""),
        language_code=request.get("language_code", "en-US"),
        voice_name=request.get("voice_name"),
        gender=VoiceGender(request.get("gender", "NEUTRAL")),
        audio_encoding=AudioEncoding(request.get("audio_encoding", "MP3")),
        speaking_rate=float(request.get("speaking_rate", 1.0)),
        pitch=float(request.get("pitch", 0.0)),
        volume_gain_db=float(request.get("volume_gain_db", 0.0)),
    )


def parse_google_tts_response(
    response, voice_name: str, language_code: str
) -> SynthesisResponse:
    """Parse Google TTS response to standardized format."""
    return SynthesisResponse(
        audio_content=response.audio_content,
        audio_encoding=AudioEncoding(response.audio_config.audio_encoding.name),
        sample_rate_hertz=response.audio_config.sample_rate_hertz,
        voice_name=voice_name,
        language_code=language_code,
    )
