from dataclasses import dataclass

@dataclass
class TranscriptChunk:
    """Represents a chunk of a live transcript."""
    text: str
    is_final: bool

    def __str__(self):
        marker = "[FINAL]" if self.is_final else "[PARTIAL]"
        return f"{marker} {self.text}"

@dataclass
class TranslatedCaption:
    """Represents a translated caption."""
    original_text: str
    translated_text: str
    target_language: str

@dataclass
class ContentSafetyResult:
    """Represents the result of a content safety check."""
    text: str
    is_safe: bool
    details: dict

@dataclass
class MeetingSummary:
    """Represents a summary of a meeting transcript portion."""
    original_text: str
    summary_text: str

@dataclass
class CaptionEmbedding:
    """Represents an embedding vector for a caption chunk."""
    text: str
    embedding: list[float]
