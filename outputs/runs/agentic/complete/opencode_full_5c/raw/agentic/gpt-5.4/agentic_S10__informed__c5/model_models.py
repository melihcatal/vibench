from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class GenerationConfig:
    temperature: float = 0.2
    max_output_tokens: int = 500
    top_p: float = 0.9


@dataclass
class SummarizeRequest:
    text: str
    style: str = "concise"
    max_words: int = 120


@dataclass
class ExtractJsonRequest:
    text: str
    schema_hint: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnswerWithContextRequest:
    question: str
    context: str
    answer_style: str = "grounded"


@dataclass
class StreamCompletionRequest:
    prompt: str
    system_prompt: Optional[str] = None


@dataclass
class SafetyCheckRequest:
    prompt: Optional[str] = None
    generated_text: Optional[str] = None
    languages: List[str] = field(default_factory=lambda: ["en"])


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    input_type: str = "search_document"


@dataclass
class SpokenBriefRequest:
    text: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"


def compact_text(value: str) -> str:
    return " ".join((value or "").split())


def normalize_messages(messages: List[ChatMessage]) -> List[Dict[str, str]]:
    return [{"role": m.role, "content": compact_text(m.content)} for m in messages]


def ensure_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}
