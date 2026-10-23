from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PromptRequest:
    text: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class JsonExtractionRequest:
    text: str
    schema_hint: Dict[str, Any] = field(default_factory=dict)
    model: Optional[str] = None


@dataclass
class ContextAnswerRequest:
    question: str
    context: str
    model: Optional[str] = None
    temperature: float = 0.0


@dataclass
class CompletionChunk:
    text: str
    finished: bool = False


@dataclass
class NormalizedResponse:
    text: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Any = None


@dataclass
class SafetyResult:
    flagged: bool
    score: float
    categories: List[str] = field(default_factory=list)
    raw: Any = None


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: Optional[str] = None


@dataclass
class SpeechRequest:
    text: str
    voice: str = "alloy"
    model: Optional[str] = None
