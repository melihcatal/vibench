from dataclasses import dataclass

@dataclass
class TranscriptChunk:
    """
    Represents a chunk of transcribed text from a streaming service.
    """
    text: str
    is_final: bool
    timestamp: float

@dataclass
class TranslatedCaption:
    """
    Represents a translated caption chunk.
    """
    original_text: str
    translated_text: str
    target_language: str

@dataclass
class SafetyAnalysisResult:
    """
    Represents the result of a content safety analysis.
    """
    is_safe: bool
    harm_categories: dict

@dataclass
class MeetingSummary:
    """
    Represents a summary of a meeting segment.
    """
    summary_text: str

@dataclass
class TextEmbedding:
    """
    Represents a text embedding vector.
    """
    text: str
    embedding: list[float]
