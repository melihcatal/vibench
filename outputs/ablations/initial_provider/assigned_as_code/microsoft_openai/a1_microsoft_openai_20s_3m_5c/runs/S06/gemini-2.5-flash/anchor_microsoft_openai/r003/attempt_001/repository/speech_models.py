from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SpeechSynthesisConfig:
    api_key: str
    region: str
    voice: str = "en-US-JennyNeural"
    output_format: str = "Audio16Khz32KBitRateMonoMp3"

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    config: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str
