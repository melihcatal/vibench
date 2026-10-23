import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class LLMRequest:
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

@dataclasses.dataclass
class LLMResponse:
    text: str
    finish_reason: Optional[str] = None

@dataclasses.dataclass
class ChatMessage:
    role: str # "user" or "model"
    content: str

@dataclasses.dataclass
class ChatRequest:
    messages: List[ChatMessage]
    max_tokens: int = 100
    temperature: float = 0.7

@dataclasses.dataclass
class ChatResponse:
    message: ChatMessage
    finish_reason: Optional[str] = None
