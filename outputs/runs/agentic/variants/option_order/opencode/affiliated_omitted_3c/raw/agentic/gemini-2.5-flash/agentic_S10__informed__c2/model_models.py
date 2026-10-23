from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class LLMRequest:
    prompt: str
    model: str
    max_tokens: int = 150
    temperature: float = 0.7


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: Dict[str, Any]


@dataclass
class EmbeddingRequest:
    text: str
    model: str


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
