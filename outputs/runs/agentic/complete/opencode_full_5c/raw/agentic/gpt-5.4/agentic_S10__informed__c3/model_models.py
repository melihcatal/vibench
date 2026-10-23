from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GenerationConfig:
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 512
    top_p: float = 0.95


@dataclass
class ChatTurn:
    role: str
    content: str


@dataclass
class LLMRequest:
    system: Optional[str] = None
    messages: List[ChatTurn] = field(default_factory=list)
    config: Optional[GenerationConfig] = None

    def to_openai_messages(self) -> List[Dict[str, str]]:
        payload: List[Dict[str, str]] = []
        if self.system:
            payload.append({"role": "system", "content": self.system})
        for turn in self.messages:
            payload.append({"role": turn.role, "content": turn.content})
        return payload


@dataclass
class LLMResponse:
    provider: str
    model: str
    text: str
    raw: Any


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def build_json_instruction(schema_hint: str) -> str:
    return normalize_whitespace(
        f"Extract the requested fields and return valid JSON only. Use this schema guidance: {schema_hint}"
    )


def choose_model(task: str) -> str:
    normalized = task.strip().lower()
    if normalized in {"summary", "summarize", "qa", "answer", "extract"}:
        return "gpt-4.1-mini"
    if normalized in {"stream", "chat"}:
        return "gpt-4.1"
    return "gpt-4.1-mini"
