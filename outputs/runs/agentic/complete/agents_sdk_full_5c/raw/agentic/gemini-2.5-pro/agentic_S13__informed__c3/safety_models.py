from dataclasses import dataclass, field
from typing import List, Tuple, Any, Dict

@dataclass
class ModerationResult:
    """Represents the result of a single text moderation."""
    is_safe: bool
    flagged_categories: List[Tuple[str, int]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RedactionResult:
    """Represents the result of a text redaction operation."""
    original_text: str
    redacted_text: str
    was_redacted: bool
    hits: List[str] = field(default_factory=list)

@dataclass
class ThresholdDecision:
    """Represents a decision based on severity thresholds."""
    allow: bool
    violated_categories: List[Tuple[str, int]] = field(default_factory=list)

@dataclass
class SummaryResult:
    """Represents a summary of moderation events."""
    summary: str
    model_used: str

@dataclass
class TranslationResult:
    """Represents a translation result."""
    original_text: str
    translated_text: str
    detected_source_lang: str

@dataclass
class EmbeddingResult:
    """Represents a text embedding result."""
    text: str
    embedding: List[float]

@dataclass
class AudioResult:
    """Represents the result of a text-to-speech operation."""
    text: str
    audio_file_path: str
