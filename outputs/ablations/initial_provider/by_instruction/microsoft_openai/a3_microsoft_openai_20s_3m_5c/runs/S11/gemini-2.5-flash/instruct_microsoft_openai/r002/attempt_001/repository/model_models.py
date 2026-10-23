from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Message:
    role: str
    content: str

@dataclass
class ModelRequest:
    messages: List[Message]
    model: str
    temperature: float = 0.7
    max_tokens: int = 150
    stream: bool = False

@dataclass
class ModelResponseChoice:
    message: Message
    index: int
    logprobs: Optional[Any] = None  # Depending on provider, can be complex
    finish_reason: str = "stop"

@dataclass
class ModelResponseUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ModelResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[ModelResponseChoice]
    usage: Optional[ModelResponseUsage] = None

