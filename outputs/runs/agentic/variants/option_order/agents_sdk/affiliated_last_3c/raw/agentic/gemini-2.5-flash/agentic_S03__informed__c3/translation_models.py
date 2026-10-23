from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranslationRequest:
    """Represents a request to translate a single text string."""
    text: str
    target_language: str
    source_language: Optional[str] = None
    format: Optional[str] = None  # e.g., 'text' or 'html'

@dataclass
class BatchTranslationRequest:
    """Represents a request to translate a list of text strings."""
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None
    format: Optional[str] = None  # e.g., 'text' or 'html'

@dataclass
class TranslationResponse:
    """Represents the response from a translation operation."""
    translated_text: str
    target_language: str
    source_language: Optional[str] = None
    original_text: Optional[str] = None

@dataclass
class TranslationQualitySummaryRequest:
    """Request for summarizing translation quality issues."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class TranslationQualitySummaryResponse:
    """Response containing the summary of translation quality issues."""
    summary: str
    issues_detected: List[str] = field(default_factory=list)
    overall_sentiment: Optional[str] = None

@dataclass
class UnsafeContentCheckRequest:
    """Request for checking localized copy for unsafe content."""
    text: str
    language: str

@dataclass
class UnsafeContentCheckResponse:
    """Response containing the safety check results."""
    is_unsafe: bool
    categories_detected: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class TranslationMemoryEmbeddingRequest:
    """Request for generating embeddings for translated segments."""
    segment: str
    language: str

@dataclass
class TranslationMemoryEmbeddingResponse:
    """Response containing the embedding vector."""
    embedding: List[float]

@dataclass
class LocalizedAudioPreviewRequest:
    """Request for generating a spoken preview of translated copy."""
    text: str
    language_code: str
    voice_name: Optional[str] = None
    audio_format: str = "wav"  # e.g., 'mp3', 'wav', 'ogg'

@dataclass
class LocalizedAudioPreviewResponse:
    """Response containing the audio content as bytes."""
    audio_content: bytes
    audio_format: str
