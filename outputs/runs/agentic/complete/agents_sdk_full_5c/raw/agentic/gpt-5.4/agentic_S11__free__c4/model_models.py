from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GenerationRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    locale: str = "en"
    safety_category: Optional[str] = None

    def to_messages(self) -> List[Dict[str, str]]:
        return [{"role": "user", "content": self.prompt}]


@dataclass
class PlatformSelection:
    project_id: str
    location: str
    model_name: str
    publisher_model: str
    endpoint: Optional[str] = None


@dataclass
class GenerationResult:
    text: str
    model: str
    provider: str = "google_vertex_ai"
    usage: Dict[str, Any] = field(default_factory=dict)
    resource: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def usage_to_dict(usage_metadata: Any) -> Dict[str, Any]:
    if usage_metadata is None:
        return {}
    fields = [
        "prompt_token_count",
        "candidates_token_count",
        "total_token_count",
        "cached_content_token_count",
    ]
    output: Dict[str, Any] = {}
    for name in fields:
        if hasattr(usage_metadata, name):
            output[name] = getattr(usage_metadata, name)
    return output


def candidate_text(response: Any) -> str:
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        texts = []
        for part in parts:
            text = getattr(part, "text", None)
            if text:
                texts.append(text)
        if texts:
            return "".join(texts).strip()
    text_attr = getattr(response, "text", None)
    if text_attr:
        return normalize_text(text_attr)
    return ""
