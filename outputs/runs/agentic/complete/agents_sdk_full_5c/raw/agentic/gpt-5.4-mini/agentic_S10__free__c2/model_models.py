from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ChatResult:
    provider: str
    model: str
    content: str


@dataclass
class JsonExtractionResult:
    provider: str
    model: str
    data: Dict[str, Any]


@dataclass
class NormalizedOutput:
    provider: str
    model: str
    text: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
