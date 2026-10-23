from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SynthesisRequest:
    text: str
    voice: str = "default"
    model: str = "CosyVoice-300M-SFT"
    text_type: str = "text"  # "text" or "ssml"


@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    sample_rate: Optional[int] = None
    channels: Optional[int] = None


@dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: str
    styles: Optional[Dict[str, Any]] = None
