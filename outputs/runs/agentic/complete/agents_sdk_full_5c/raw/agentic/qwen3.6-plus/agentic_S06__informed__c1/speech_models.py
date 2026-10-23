"""
Local helper: speech_models.py
Define local request, response, and normalization helpers for Text-to-Speech.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import base64
import io


class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"
    PCM = "pcm"


class VoiceGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


@dataclass
class TTSRequest:
    """Normalized text-to-speech request model."""
    text: str
    voice_id: str = "default"
    model_id: str = "eleven_multilingual_v2"
    audio_format: AudioFormat = AudioFormat.MP3
    speed: float = 1.0
    pitch: float = 0.0
    stability: float = 0.5
    similarity_boost: float = 0.75
    ssml: bool = False
    language_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "audio_format": self.audio_format.value,
            "speed": self.speed,
            "pitch": self.pitch,
            "stability": self.stability,
            "similarity_boost": self.similarity_boost,
            "ssml": self.ssml,
            "language_code": self.language_code,
        }


@dataclass
class SSMLRequest:
    """Normalized SSML synthesis request model."""
    ssml: str
    voice_id: str = "default"
    model_id: str = "eleven_multilingual_v2"
    audio_format: AudioFormat = AudioFormat.MP3
    speed: float = 1.0
    pitch: float = 0.0
    stability: float = 0.5
    similarity_boost: float = 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ssml": self.ssml,
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "audio_format": self.audio_format.value,
            "speed": self.speed,
            "pitch": self.pitch,
            "stability": self.stability,
            "similarity_boost": self.similarity_boost,
        }


@dataclass
class TTSResponse:
    """Normalized text-to-speech response model."""
    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    voice_id: str = ""
    model_id: str = ""
    duration_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def audio_base64(self) -> str:
        return base64.b64encode(self.audio_bytes).decode("utf-8")

    @property
    def file_extension(self) -> str:
        extensions = {
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg",
            "audio/flac": ".flac",
            "audio/pcm": ".pcm",
        }
        return extensions.get(self.content_type, ".mp3")

    def to_audio_stream(self) -> io.BytesIO:
        return io.BytesIO(self.audio_bytes)


@dataclass
class VoiceInfo:
    """Normalized voice information model."""
    voice_id: str
    name: str
    language_code: str
    gender: VoiceGender = VoiceGender.NEUTRAL
    preview_url: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    category: str = "premade"
    description: Optional[str] = None


@dataclass
class VoiceListResponse:
    """Normalized voice list response model."""
    voices: List[VoiceInfo] = field(default_factory=list)
    total_count: int = 0


def normalize_audio_format(format_str: str) -> AudioFormat:
    """Normalize audio format string to AudioFormat enum."""
    format_map = {
        "mp3": AudioFormat.MP3,
        "wav": AudioFormat.WAV,
        "ogg": AudioFormat.OGG,
        "flac": AudioFormat.FLAC,
        "pcm": AudioFormat.PCM,
        "audio/mpeg": AudioFormat.MP3,
        "audio/wav": AudioFormat.WAV,
        "audio/ogg": AudioFormat.OGG,
        "audio/flac": AudioFormat.FLAC,
    }
    return format_map.get(format_str.lower(), AudioFormat.MP3)


def wrap_ssml(text: str, voice_name: Optional[str] = None,
              rate: Optional[str] = None, pitch: Optional[str] = None,
              volume: Optional[str] = None) -> str:
    """Wrap plain text in SSML with optional prosody controls."""
    prosody_attrs = ""
    if rate:
        prosody_attrs += f' rate="{rate}"'
    if pitch:
        prosody_attrs += f' pitch="{pitch}"'
    if volume:
        prosody_attrs += f' volume="{volume}"'

    ssml = '<?xml version="1.0"?>'
    if voice_name:
        ssml += f'<speak><voice name="{voice_name}">'
    else:
        ssml += "<speak>"

    if prosody_attrs:
        ssml += f"<prosody{prosody_attrs}>{text}</prosody>"
    else:
        ssml += text

    if voice_name:
        ssml += "</voice></speak>"
    else:
        ssml += "</speak>"

    return ssml
