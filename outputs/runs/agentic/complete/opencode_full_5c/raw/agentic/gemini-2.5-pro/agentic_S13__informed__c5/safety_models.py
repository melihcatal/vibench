from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ModerationResult:
    """
    Represents the result of a single text moderation.
    """

    passed: bool
    category_scores: Dict[str, int]
    text: str


@dataclass
class BatchModerationResult:
    """
    Represents the result of a batch text moderation.
    """

    results: List[ModerationResult]


@dataclass
class RedactionResult:
    """
    Represents the result of a text redaction.
    """

    original_text: str
    redacted_text: str
    flagged_spans: List[dict]


@dataclass
class SummaryResult:
    """
    Represents the summary of moderation decisions.
    """

    summary: str


@dataclass
class TranslationResult:
    """
    Represents the result of a text translation.
    """

    original_text: str
    translated_text: str
    target_language: str


@dataclass
class EmbeddingResult:
    """
    Represents the result of text embedding.
    """

    embeddings: List[List[float]]


@dataclass
class AudioResult:
    """
    Represents the result of audio generation.
    """

    audio_file_path: str
