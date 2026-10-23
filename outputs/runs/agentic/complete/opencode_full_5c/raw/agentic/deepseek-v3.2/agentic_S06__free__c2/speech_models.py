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
    """Request model for text-to-speech synthesis."""

    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: str = "en-US-Neural2-J"
    voice_gender: VoiceGender = VoiceGender.NEUTRAL
    audio_encoding: AudioEncoding = AudioEncoding.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    sample_rate_hertz: Optional[int] = None


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
    language_code: str
    gender: VoiceGender
    natural_sample_rate_hertz: int
    supported_audio_encodings: list[AudioEncoding]


def normalize_synthesis_request(request: Dict[str, Any]) -> SynthesisRequest:
    """Normalize synthesis request from dictionary."""
    return SynthesisRequest(
        text=request.get("text"),
        ssml=request.get("ssml"),
        language_code=request.get("language_code", "en-US"),
        voice_name=request.get("voice_name", "en-US-Neural2-J"),
        voice_gender=VoiceGender(request.get("voice_gender", "NEUTRAL")),
        audio_encoding=AudioEncoding(request.get("audio_encoding", "MP3")),
        speaking_rate=float(request.get("speaking_rate", 1.0)),
        pitch=float(request.get("pitch", 0.0)),
        volume_gain_db=float(request.get("volume_gain_db", 0.0)),
        sample_rate_hertz=request.get("sample_rate_hertz"),
    )


def create_ssml_from_text(
    text: str, voice_params: Optional[Dict[str, Any]] = None
) -> str:
    """Create SSML from plain text with optional voice parameters."""
    if voice_params:
        speaking_rate = voice_params.get("speaking_rate", 1.0)
        pitch = voice_params.get("pitch", 0.0)
        volume = voice_params.get("volume", "medium")

        ssml = f"""<speak>
<prosody rate="{speaking_rate}" pitch="{pitch}" volume="{volume}">
{text}
</prosody>
</speak>"""
    else:
        ssml = f"<speak>{text}</speak>"

    return ssml
