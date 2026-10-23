from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SynthesizeTextRequest:
    text: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    region: Optional[str] = None


@dataclass
class SynthesizeSSMLRequest:
    ssml: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    region: Optional[str] = None


@dataclass
class SelectVoiceRequest:
    language_code: Optional[str] = None
    gender: Optional[str] = None  # "Male" or "Female"
    region: Optional[str] = None


@dataclass
class SaveAudioRequest:
    audio_bytes: bytes
    file_key: str
    content_type: str = "audio/mpeg"
    s3_bucket_name: Optional[str] = None
    region: Optional[str] = None


@dataclass
class SynthesizeResponse:
    audio_bytes: bytes
    content_type: str


@dataclass
class VoiceInfo:
    id: str
    name: str
    gender: str
    language_code: str


@dataclass
class SelectVoiceResponse:
    voices: list[VoiceInfo]


@dataclass
class SaveAudioResponse:
    s3_uri: str
