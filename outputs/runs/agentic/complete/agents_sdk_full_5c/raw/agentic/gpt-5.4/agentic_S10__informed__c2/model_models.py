from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str

    def to_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class LLMRequest:
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    stream: bool = False

    def normalized_messages(self) -> List[Dict[str, str]]:
        return [message.to_openai() for message in self.messages]


@dataclass
class LLMResponse:
    model: str
    content: str
    raw: Any = None


@dataclass
class SafetyResult:
    scores: Dict[str, float] = field(default_factory=dict)
    flagged: bool = False
    raw: Any = None


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    raw: Any = None


@dataclass
class SpeechResult:
    audio_bytes: bytes
    content_type: str
    raw: Any = None


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2:
            if lines[-1].strip() == "```":
                return "\n".join(lines[1:-1]).strip()
    return cleaned
