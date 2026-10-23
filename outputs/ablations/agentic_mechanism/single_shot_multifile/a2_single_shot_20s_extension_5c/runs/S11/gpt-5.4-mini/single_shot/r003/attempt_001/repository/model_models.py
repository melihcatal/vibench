from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


@dataclass
class PlatformRequest:
    prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class PlatformResponse:
    text: str
    model: str
    response: Any


@dataclass
class PlatformStreamChunk:
    event: Any
    model: str


@dataclass
class PlatformMetadataResult:
    text: str
    model: str
    resource_id: str
    usage: Dict[str, Any]
    raw_response: Any
