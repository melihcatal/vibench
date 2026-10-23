from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformPrompt:
    messages: List[Dict[str, str]]
    model_hint: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 1024


@dataclass
class PlatformSelection:
    project_id: str
    resource_id: str
    model_name: str
    deployment_name: Optional[str] = None
    inference_profile_id: Optional[str] = None


@dataclass
class PlatformResponse:
    text: str
    model: Optional[str] = None
    resource_id: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class StreamingChunk:
    text: str
    raw: Any = None


@dataclass
class NormalizedPlatformResult:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    is_safe: bool
    provider: str
    categories: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_locale: str
    provider: str
    raw: Any = None


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]
    provider: str
    raw: Any = None


@dataclass
class AudioBriefResult:
    text: str
    audio_bytes: bytes
    provider: str
    content_type: str = "audio/mpeg"
    raw: Any = None


def normalize_messages(messages: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for msg in messages:
        role = str(msg.get("role", "user")).strip()
        content = str(msg.get("content", ""))
        normalized.append({"role": role, "content": content})
    return normalized


def extract_text_from_choice(choice: Any) -> str:
    message = getattr(choice, "message", None)
    if message is not None and getattr(message, "content", None):
        return message.content
    delta = getattr(choice, "delta", None)
    if delta is not None and getattr(delta, "content", None):
        return delta.content
    if isinstance(choice, dict):
        if "message" in choice and choice["message"].get("content"):
            return choice["message"]["content"]
        if "delta" in choice and choice["delta"].get("content"):
            return choice["delta"]["content"]
    return ""
