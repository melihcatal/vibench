from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingUtterance:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None


@dataclass
class StreamingRequest:
    language: str = "en-US"
    punctuate: bool = True
    model: str = "nova-2"


@dataclass
class StreamingResponse:
    text: str
    is_final: bool
    raw: Optional[Dict[str, Any]] = None


def normalize_caption(text: str) -> str:
    return " ".join((text or "").strip().split())


def to_response(payload: Any) -> StreamingResponse:
    text = normalize_caption(getattr(payload, "text", "") or getattr(payload, "transcript", ""))
    return StreamingResponse(text=text, is_final=bool(getattr(payload, "is_final", False)), raw=getattr(payload, "raw", None))
