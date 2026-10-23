from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class AudioFormat(str, Enum):
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
class TextToSpeechRequest:
    text: str
    voice_id: str = "en-US-Neural2-J"
    language_code: str = "en-US"
    audio_format: AudioFormat = AudioFormat.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: str = "en-US-Neural2-J"
    language_code: str = "en-US"
    audio_format: AudioFormat = AudioFormat.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class AudioResponse:
    audio_content: bytes
    audio_format: AudioFormat
    sample_rate_hertz: int
    voice_name: str
    language_code: str


@dataclass
class VoiceInfo:
    name: str
    language_codes: list[str]
    ssml_gender: VoiceGender
    natural_sample_rate_hertz: int


def normalize_audio_format(format_str: str) -> AudioFormat:
    """Normalize audio format string to enum."""
    format_str = format_str.upper().replace("-", "_")
    try:
        return AudioFormat(format_str)
    except ValueError:
        return AudioFormat.MP3


def normalize_gender(gender_str: str) -> VoiceGender:
    """Normalize gender string to enum."""
    gender_str = gender_str.upper()
    try:
        return VoiceGender(gender_str)
    except ValueError:
        return VoiceGender.NEUTRAL


def create_ssml(text: str, voice_params: Optional[Dict[str, Any]] = None) -> str:
    """Create SSML markup from plain text with optional voice parameters."""
    if voice_params is None:
        voice_params = {}

    rate = voice_params.get("speaking_rate", 1.0)
    pitch = voice_params.get("pitch", 0.0)
    volume = voice_params.get("volume", 0.0)

    ssml = f"""<speak>
    <prosody rate="{rate}" pitch="{pitch}dB" volume="{volume}dB">
        {text}
    </prosody>
</speak>"""

    return ssml
