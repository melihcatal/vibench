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
class InferenceRequest:
    system_prompt: Optional[str] = None
    user_prompt: str = ""
    temperature: float = 0.2
    max_tokens: int = 400
    model: Optional[str] = None
    context: Optional[str] = None

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append(ChatMessage(role="system", content=self.system_prompt).to_openai())
        if self.context:
            messages.append(
                ChatMessage(role="user", content=f"Context:\n{self.context}\n\nTask:\n{self.user_prompt}").to_openai()
            )
        else:
            messages.append(ChatMessage(role="user", content=self.user_prompt).to_openai())
        return messages


@dataclass
class InferenceResponse:
    text: str
    model: str
    finish_reason: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str
    dimensions: Optional[int] = None


@dataclass
class SafetyCheckResult:
    flagged: bool
    provider: str
    scores: Dict[str, float] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned
