from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ModerationScore:
    attribute: str
    score: float


@dataclass
class ModerationResult:
    text: str
    scores: List[ModerationScore]
    is_unsafe: bool = False
    unsafe_attributes: List[str] = ""


@dataclass
class RedactionSpan:
    begin: int
    end: int
    original_text: str
    redacted_text: str


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    redaction_spans: List[RedactionSpan]


@dataclass
class ModerationSummary:
    original_decisions: List[ModerationResult]
    summary_text: str


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]


@dataclass
class AudioBriefResult:
    text: str
    audio_content: bytes
