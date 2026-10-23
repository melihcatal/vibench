from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class LLMRequest:
    prompt: str
    model: str = "gpt-5.4-mini"
    temperature: float = 0.7
    max_tokens: int = 150

@dataclass
class LLMResponse:
    text: str
    raw_response: Dict[str, Any]

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class ChatCompletionRequest:
    messages: List[ChatMessage]
    model: str = "gpt-5.4-mini"
    temperature: float = 0.7
    max_tokens: int = 150
