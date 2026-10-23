from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SynthesisPayload:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-JennyNeural"
    output_format: str = "Audio16Khz32KBitRateMonoMp3"

@dataclass
class TranslationPayload:
    text: str
    from_language: str
    to_language: str

@dataclass
class ContentModerationPayload:
    text: str

@dataclass
class EmbeddingPayload:
    text: str

@dataclass
class TranscriptionPayload:
    audio_bytes: bytes
    audio_format: str = "audio/mpeg"
    language: str = "en-US"
