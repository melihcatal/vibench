from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class InvokeRequest:
    prompt: str


@dataclass
class InvokeResponse:
    text: str
    metadata: Dict[str, Any]


@dataclass
class StreamChunk:
    text: str
    raw_chunk: Any
