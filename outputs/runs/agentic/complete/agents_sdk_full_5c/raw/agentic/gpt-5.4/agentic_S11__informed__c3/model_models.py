from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    system: Optional[str] = None
    max_tokens: int = 256
    temperature: float = 0.2
    top_p: float = 0.95

    def to_openai_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class ModelChoice:
    index: int
    text: str
    finish_reason: Optional[str] = None


@dataclass
class ModelResult:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    choices: List[ModelChoice] = field(default_factory=list)
    raw: Any = None


@dataclass
class StreamChunk:
    text: str
    raw: Any = None
    done: bool = False


@dataclass
class SafetyResult:
    safe: bool
    category_scores: Dict[str, float]
    raw: Any = None


@dataclass
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    raw: Any = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    raw: Any = None


@dataclass
class AudioBriefResult:
    audio_bytes: bytes
    content_type: str
    raw: Any = None


def first_text_from_choices(choices: Iterable[Any]) -> str:
    for choice in choices:
        message = getattr(choice, "message", None)
        if message is not None and getattr(message, "content", None):
            content = message.content
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    elif hasattr(item, "text"):
                        parts.append(getattr(item, "text", ""))
                return "".join(parts)
        text = getattr(choice, "text", None)
        if text:
            return text
    return ""


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return dict(usage)
    result: Dict[str, Any] = {}
    for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, name, None)
        if value is not None:
            result[name] = value
    return result
