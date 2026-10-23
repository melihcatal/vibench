from dataclasses import dataclass
from typing import Optional

@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None

@dataclass
class TranslationRequest:
    text: str
    target_language: str

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    is_unsafe: bool
    categories: dict

@dataclass
class SummaryRequest:
    transcript_chunk: str

@dataclass
class SummaryResponse:
    summary: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: list[float]