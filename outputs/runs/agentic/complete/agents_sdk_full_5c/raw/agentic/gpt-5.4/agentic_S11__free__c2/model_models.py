from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatRequest:
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512
    resource_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class ChatResult:
    text: str
    model: str
    resource_name: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class SafetyResult:
    safe: bool
    categories: List[str] = field(default_factory=list)
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    model: str
    dimensions: int
    raw: Any = None


@dataclass
class AudioResult:
    audio_base64: str
    format: str
    voice: str
    raw: Any = None


@dataclass
class TranslationResult:
    text: str
    target_locale: str
    model: str
    raw: Any = None


def usage_to_dict(usage: Any) -> Dict[str, Any]:
    if usage is None:
        return {}
    if isinstance(usage, dict):
        return usage
    data: Dict[str, Any] = {}
    for key in (
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_tokens",
    ):
        value = getattr(usage, key, None)
        if value is not None:
            data[key] = value
    if not data and hasattr(usage, "model_dump"):
        return usage.model_dump()
    return data


def extract_text_from_response(response: Any) -> str:
    if response is None:
        return ""
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text
    output = getattr(response, "output", None) or []
    collected: List[str] = []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if text:
                collected.append(text)
    return "".join(collected)
