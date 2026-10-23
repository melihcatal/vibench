from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class CompletionRequest:
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 150

@dataclass
class CompletionResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]

@dataclass
class EmbeddingRequest:
    model: str
    input: str | List[str]

@dataclass
class EmbeddingResponse:
    object: str
    data: List[Dict[str, Any]]
    model: str
    usage: Dict[str, int]
