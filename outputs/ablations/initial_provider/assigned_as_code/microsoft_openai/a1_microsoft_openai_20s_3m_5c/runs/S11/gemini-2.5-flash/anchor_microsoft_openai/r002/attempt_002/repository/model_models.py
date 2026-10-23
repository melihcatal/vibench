from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class ModelRequest:
    messages: List[ChatMessage]
    model: str
    stream: Optional[bool] = False

@dataclass
class ModelResponseChoice:
    message: ChatMessage
    finish_reason: str

@dataclass
class ModelResponseUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ModelResponse:
    id: str
    model: str
    choices: List[ModelResponseChoice]
    usage: ModelResponseUsage
    created: int
