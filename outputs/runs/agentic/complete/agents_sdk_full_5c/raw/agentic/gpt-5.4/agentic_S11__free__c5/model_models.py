from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class PlatformRequest:
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.2
    system: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_messages(self) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass(slots=True)
class PlatformSelection:
    project_id: str
    location: str
    model: str
    publisher: str = "google"

    @property
    def resource_name(self) -> str:
        return (
            f"projects/{self.project_id}/locations/{self.location}"
            f"/publishers/{self.publisher}/models/{self.model}"
        )


@dataclass(slots=True)
class PlatformResult:
    text: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)



def join_text_parts(parts: Iterable[Any]) -> str:
    chunks: List[str] = []
    for part in parts:
        text = getattr(part, "text", None)
        if text:
            chunks.append(text)
            continue
        if isinstance(part, dict) and part.get("text"):
            chunks.append(str(part["text"]))
    return "".join(chunks)



def candidate_text(candidate: Any) -> str:
    content = getattr(candidate, "content", None)
    if content is not None:
        parts = getattr(content, "parts", [])
        return join_text_parts(parts)
    if isinstance(candidate, dict):
        content = candidate.get("content", {})
        return join_text_parts(content.get("parts", []))
    return ""



def extract_usage_metadata(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage_metadata", None)
    if usage is None and isinstance(response, dict):
        usage = response.get("usage_metadata", {})
    if usage is None:
        return {}
    keys = [
        "prompt_token_count",
        "candidates_token_count",
        "total_token_count",
        "cached_content_token_count",
    ]
    data: Dict[str, Any] = {}
    for key in keys:
        value = getattr(usage, key, None)
        if value is None and isinstance(usage, dict):
            value = usage.get(key)
        if value is not None:
            data[key] = value
    return data
