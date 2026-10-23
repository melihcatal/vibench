from dataclasses import dataclass
from typing import List


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatRequest:
    messages: List[ChatMessage]
    model: str = "gpt-4o"
    temperature: float = 0.7


@dataclass
class ChatResponse:
    text: str


@dataclass
class EmbeddingResponse:
    embedding: List[float]
