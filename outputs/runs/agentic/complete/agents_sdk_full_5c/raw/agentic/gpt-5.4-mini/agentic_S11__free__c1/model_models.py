from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class PlatformRequest:
    input_text: str
    model: str
    resource_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model, "input": self.input_text}
        if self.resource_id:
            payload["resource_id"] = self.resource_id
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


@dataclass
class NormalizedChunk:
    text: str
    raw: Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            parts.append(normalize_text(item))
        return "".join(parts)
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        if "content" in value:
            return normalize_text(value["content"])
        return " ".join(normalize_text(v) for v in value.values())
    return str(value)


def dict_from_dataclass(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
