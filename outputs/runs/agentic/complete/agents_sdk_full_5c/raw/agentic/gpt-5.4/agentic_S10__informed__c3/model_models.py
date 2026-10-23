from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class ChatTurn:
    role: str
    content: str


@dataclass(slots=True)
class GenerationConfig:
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_output_tokens: int = 500


@dataclass(slots=True)
class SummaryRequest:
    text: str
    system_prompt: str = "You summarize long-form text into concise, faithful summaries."
    config: GenerationConfig = field(default_factory=GenerationConfig)


@dataclass(slots=True)
class ExtractionRequest:
    text: str
    schema_hint: Dict[str, Any]
    system_prompt: str = "Extract the requested structured data and return valid JSON only."
    config: GenerationConfig = field(default_factory=GenerationConfig)


@dataclass(slots=True)
class ContextAnswerRequest:
    question: str
    context: str
    system_prompt: str = "Answer only from the provided context. If the answer is not in the context, say you do not know."
    config: GenerationConfig = field(default_factory=GenerationConfig)


@dataclass(slots=True)
class LLMTextResponse:
    text: str
    model: str
    provider: str = "openai"
    raw: Optional[Any] = None


@dataclass(slots=True)
class SafetyCheckResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    raw: Optional[Dict[str, Any]] = None


@dataclass(slots=True)
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None
    raw: Optional[Any] = None


@dataclass(slots=True)
class EmbeddingResult:
    provider: str
    model: str
    embeddings: List[List[float]]
    raw: Optional[Any] = None


@dataclass(slots=True)
class SpeechResult:
    provider: str
    audio_bytes: bytes
    content_type: str
    voice: str


def join_text_parts(parts: Iterable[str]) -> str:
    return "".join(part for part in parts if part)


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())
