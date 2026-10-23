from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class AudioEncoding(str, Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"


class VoiceGender(str, Enum):
    NEUTRAL = "NEUTRAL"
    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass
class SynthesisRequest:
    """Request model for text-to-speech synthesis."""

    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    voice_gender: VoiceGender = VoiceGender.NEUTRAL
    audio_encoding: AudioEncoding = AudioEncoding.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass
class SynthesisResponse:
    """Response model for text-to-speech synthesis."""

    audio_content: bytes
    audio_encoding: AudioEncoding
    sample_rate_hertz: int
    voice_name: str
    language_code: str


@dataclass
class VoiceInfo:
    """Voice information model."""

    name: str
    language_codes: List[str]
    ssml_gender: VoiceGender
    natural_sample_rate_hertz: int


def normalize_synthesis_request(request: Dict[str, Any]) -> SynthesisRequest:
    """Normalize synthesis request from dictionary."""
    return SynthesisRequest(
        text=request.get("text", ""),
        language_code=request.get("language_code", "en-US"),
        voice_name=request.get("voice_name"),
        voice_gender=VoiceGender(request.get("voice_gender", "NEUTRAL")),
        audio_encoding=AudioEncoding(request.get("audio_encoding", "MP3")),
        speaking_rate=float(request.get("speaking_rate", 1.0)),
        pitch=float(request.get("pitch", 0.0)),
        volume_gain_db=float(request.get("volume_gain_db", 0.0)),
    )


def normalize_voice_info(voice_data: Dict[str, Any]) -> VoiceInfo:
    """Normalize voice information from dictionary."""
    return VoiceInfo(
        name=voice_data.get("name", ""),
        language_codes=voice_data.get("language_codes", []),
        ssml_gender=VoiceGender(voice_data.get("ssml_gender", "NEUTRAL")),
        natural_sample_rate_hertz=voice_data.get("natural_sample_rate_hertz", 24000),
    )


def create_ssml_from_text(
    text: str,
    voice_name: str = "en-US-Neural2-J",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> str:
    """Create SSML markup from plain text with prosody controls."""
    return f"""<speak>
    <voice name="{voice_name}">
        <prosody rate="{speaking_rate}" pitch="{pitch}">
            {text}
        </prosody>
    </voice>
</speak>"""
