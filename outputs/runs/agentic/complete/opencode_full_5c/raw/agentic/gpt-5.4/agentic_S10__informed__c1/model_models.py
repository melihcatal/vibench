from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ChatRequest:
    system_prompt: str
    user_prompt: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class ChatResponse:
    text: str
    model: str
    provider: str
    finish_reason: Optional[str] = None


@dataclass
class SafetyResult:
    provider: str
    blocked: bool
    scores: Dict[str, float]
    flagged_categories: List[str]


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int


@dataclass
class SpeechResult:
    provider: str
    audio_bytes: bytes
    content_type: str
    voice_id: str


def truncate_text(text: str, max_chars: int = 20000) -> str:
    return text if len(text) <= max_chars else text[:max_chars]


def join_context_parts(parts: Iterable[str]) -> str:
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def normalize_json_text(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            stripped = "\n".join(lines[1:-1]).strip()
    return stripped


def as_message_payload(system_prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
