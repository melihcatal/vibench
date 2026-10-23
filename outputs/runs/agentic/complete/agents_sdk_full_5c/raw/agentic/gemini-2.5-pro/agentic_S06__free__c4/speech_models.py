"""
Defines local request, response, and normalization helpers for Text-to-Speech.

These data classes provide a common structure for handling data across different
TTS provider APIs, simplifying the application logic.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class Voice:
    """Represents a TTS voice from any provider."""
    id: str
    name: str
    gender: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None

@dataclass
class SynthesisRequest:
    """Represents a generic TTS request."""
    text: str
    voice_id: str
    is_ssml: bool = False

@dataclass
class AudioResponse:
    """Represents the audio output from a TTS provider."""
    content: bytes
    content_type: str # e.g., 'audio/mpeg'

@dataclass
class TranslationResponse:
    """Represents a translation result."""
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class SafetyCheckResponse:
    """Represents a content safety check result."""
    is_flagged: bool
    details: Dict[str, Any]

@dataclass
class EmbeddingResponse:
    """Represents an embedding result."""
    embedding: List[float]
    model: str

@dataclass
class TranscriptionResponse:
    """Represents a transcription result."""
    text: str
    confidence: Optional[float] = None
