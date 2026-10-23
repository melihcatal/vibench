from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformMessage:
    role: str
    content: str

    def to_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 512
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class GenerationResult:
    text: str
    model: Optional[str] = None
    resource: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class SafetyResult:
    is_safe: bool
    scores: Dict[str, float]
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    dimensions: int
    raw: Any = None


def extract_text_from_chat_completion(response: Any) -> str:
    if hasattr(response, "choices") and response.choices:
        message = getattr(response.choices[0], "message", None)
        if message and getattr(message, "content", None):
            return message.content
        delta = getattr(response.choices[0], "delta", None)
        if delta and getattr(delta, "content", None):
            return delta.content
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            if message.get("content"):
                return message["content"]
    return ""


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    result: Dict[str, Any] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, key, None)
        if value is not None:
            result[key] = value
    return result
