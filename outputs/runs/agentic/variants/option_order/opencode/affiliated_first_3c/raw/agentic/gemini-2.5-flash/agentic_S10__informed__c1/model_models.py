import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class ChatRequest:
    prompt: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclasses.dataclass
class ChatResponse:
    text: str


@dataclasses.dataclass
class Message:
    role: str
    parts: List[Dict[str, Any]]


@dataclasses.dataclass
class Conversation:
    messages: List[Message]
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclasses.dataclass
class EmbedRequest:
    text: str
    model: str = "embedding-001"


@dataclasses.dataclass
class EmbedResponse:
    embedding: List[float]
