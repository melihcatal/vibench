from typing import NamedTuple

class TranscriptResult(NamedTuple):
    """Represents a partial or final transcript result."""
    text: str
    is_final: bool

class TranslationResult(NamedTuple):
    """Represents a translation result."""
    original_text: str
    translated_text: str
    source_language: str

class ContentSafetyResult(NamedTuple):
    """Represents a content safety analysis result."""
    text: str
    is_safe: bool
    scores: dict

class SummaryResult(NamedTuple):
    """Represents a summarization result."""
    original_text: str
    summary: str

class EmbeddingResult(NamedTuple):
    """Represents a text embedding result."""
    text: str
    embedding: list[float]
