from dataclasses import dataclass, field
from typing import List, Literal, Optional

@dataclass
class AudioChunk:
    chunk_id: str
    audio_content: bytes
    sample_rate_hertz: int

@dataclass
class SpeechRecognitionConfig:
    encoding: Literal['LINEAR16', 'FLAC', 'MULAW']
    sample_rate_hertz: int
    language_code: str
    enable_automatic_punctuation: bool = False

@dataclass
class StreamingRecognitionResult:
    transcript: str
    is_final: bool
    language_code: Optional[str] = None
    confidence: Optional[float] = None

@dataclass
class TranslationConfig:
    source_language_code: str
    target_language_code: str

@dataclass
class SafetyCheckResult:
    safe: bool
    scores: dict = field(default_factory=dict)

@dataclass
class SummaryResult:
    summary: str

@dataclass
class EmbeddingResult:
    embedding: List[float]
