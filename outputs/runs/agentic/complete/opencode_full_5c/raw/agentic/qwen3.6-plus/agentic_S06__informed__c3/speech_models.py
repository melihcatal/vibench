from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TTSRequest:
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    speaker_boost: bool = True


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    model_id: str = ""
    voice_id: str = ""
    character_count: int = 0


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    locale: str = ""
    gender: str = ""
    preview_url: str = ""
    category: str = ""


@dataclass
class SSMLRequest:
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    output_format: str = "mp3_44100_128"
    speed: float = 1.0
    pitch: float = 0.0
    volume_db: float = 0.0


def normalize_request(text: str, **kwargs) -> TTSRequest:
    from speech_client import get_default_voice_id, get_default_model_id

    return TTSRequest(
        text=text.strip(),
        voice_id=kwargs.get("voice_id") or get_default_voice_id(),
        model_id=kwargs.get("model_id") or get_default_model_id(),
        output_format=kwargs.get("output_format", "mp3_44100_128"),
        stability=kwargs.get("stability", 0.5),
        similarity_boost=kwargs.get("similarity_boost", 0.75),
        style=kwargs.get("style", 0.0),
        speaker_boost=kwargs.get("speaker_boost", True),
    )


def normalize_ssml_request(text: str, **kwargs) -> SSMLRequest:
    from speech_client import get_default_voice_id, get_default_model_id

    return SSMLRequest(
        text=text.strip(),
        voice_id=kwargs.get("voice_id") or get_default_voice_id(),
        model_id=kwargs.get("model_id") or get_default_model_id(),
        output_format=kwargs.get("output_format", "mp3_44100_128"),
        speed=kwargs.get("speed", 1.0),
        pitch=kwargs.get("pitch", 0.0),
        volume_db=kwargs.get("volume_db", 0.0),
    )


def normalize_voice_info(raw_voice: dict) -> VoiceInfo:
    return VoiceInfo(
        voice_id=raw_voice.get("voice_id", ""),
        name=raw_voice.get("name", ""),
        locale=raw_voice.get("labels", {}).get("locale", "")
        or raw_voice.get("labels", {}).get("accent", ""),
        gender=raw_voice.get("labels", {}).get("gender", ""),
        preview_url=raw_voice.get("preview_url", ""),
        category=raw_voice.get("category", ""),
    )
