import dataclasses
from typing import Optional, List, Dict, Any


@dataclasses.dataclass
class VoiceConfig:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None  # For Google Cloud: MALE, FEMALE, NEUTRAL


@dataclasses.dataclass
class AudioConfig:
    audio_encoding: str  # For Google Cloud: LINEAR16, MP3, OGG_OPUS
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None


@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclasses.dataclass
class TranslationOutput:
    translated_text: str
    detected_language_code: str


@dataclasses.dataclass
class SafetyRating:
    category: str
    score: float


@dataclasses.dataclass
class SafetyAssessment:
    ratings: List[SafetyRating]


@dataclasses.dataclass
class EmbeddingOutput:
    embedding: List[float]


@dataclasses.dataclass
class TranscriptionOutput:
    transcript: str
    confidence: float
