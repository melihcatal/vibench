from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class FinishReason(str, Enum):
    LENGTH = "length"
    STOP = "stop"
    ERROR = "error"


@dataclass
class ModelRequest:
    model_id: str
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    stop_sequences: Optional[List[str]] = None


@dataclass
class ModelResponse:
    output: str
    details: Dict[str, Any]


@dataclass
class ModelResponseWithMetadata:
    output: str
    metadata: Dict[str, Any]


@dataclass
class StreamChunk:
    text: str
    details: Dict[str, Any]
