from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class TTSRequest:
    text: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    category: str
    language_codes: List[str] = field(default_factory=list)
    description: str = ""
    preview_url: Optional[str] = None


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str
    model_used: str
    voice_used: str


@dataclass
class VoiceSelectionResult:
    voice_id: str
    name: str
    locale: str
    gender: str


def normalize_voice_data(raw_voice) -> VoiceInfo:
    return VoiceInfo(
        voice_id=raw_voice.voice_id,
        name=raw_voice.name,
        category=raw_voice.category or "",
        language_codes=list(raw_voice.labels.keys()) if raw_voice.labels else [],
        description=raw_voice.description or "",
        preview_url=raw_voice.preview_url,
    )


def build_tts_response(audio_bytes: bytes, model_id: str, voice_id: str) -> TTSResponse:
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_used=model_id,
        voice_used=voice_id,
    )
