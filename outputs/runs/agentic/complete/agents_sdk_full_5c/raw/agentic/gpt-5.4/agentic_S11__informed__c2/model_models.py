from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlatformMessage:
    role: str
    content: str

    def as_openai(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationRequest:
    messages: List[PlatformMessage]
    temperature: float = 0.2
    max_output_tokens: int = 256

    def as_chat_payload(self) -> List[Dict[str, str]]:
        return [message.as_openai() for message in self.messages]


@dataclass
class GenerationResult:
    text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    provider_response_id: Optional[str] = None
    resource: Optional[str] = None


@dataclass
class SafetyResult:
    safe: bool
    scores: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class TranslationResult:
    text: str
    target_language: str
    detected_source_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    dimensions: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioBriefResult:
    audio_bytes: bytes
    content_type: str
    voice: str
    raw: Dict[str, Any] = field(default_factory=dict)


def extract_text_from_chat_completion(response: Any) -> str:
    if getattr(response, "choices", None):
        message = response.choices[0].message
        if message and getattr(message, "content", None):
            return message.content
    return ""


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if isinstance(usage, dict):
        return usage
    data: Dict[str, Any] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, key, None)
        if value is not None:
            data[key] = value
    return data
