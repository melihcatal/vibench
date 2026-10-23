from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TTSRequest:
    text: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    provider: str = "elevenlabs"

    def normalize(self) -> dict:
        return {
            "text": self.text.strip(),
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "output_format": self.output_format,
            "voice_settings": {
                "stability": max(0.0, min(1.0, self.stability)),
                "similarity_boost": max(0.0, min(1.0, self.similarity_boost)),
                "style": max(0.0, min(1.0, self.style)),
            },
        }


@dataclass
class TTSResponse:
    audio_data: bytes
    voice_id: str
    model_id: str
    format: str
    provider: str = "elevenlabs"
    duration_ms: Optional[float] = None
    character_count: Optional[int] = None


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    locale: str
    gender: str
    accent: str
    description: str
    provider: str = "elevenlabs"


@dataclass
class VoiceListResponse:
    voices: List[VoiceInfo]
    provider: str = "elevenlabs"


def normalize_ssml(ssml: str) -> str:
    if not ssml.strip().startswith("<speak"):
        ssml = f'<speak version="1.0">{ssml}</speak>'
    return ssml


def estimate_character_count(text: str) -> int:
    return len(text)
