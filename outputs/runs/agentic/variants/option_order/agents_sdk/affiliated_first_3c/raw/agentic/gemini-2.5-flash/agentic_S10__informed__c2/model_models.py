import dataclasses
from typing import Dict, Any, List, Optional

@dataclasses.dataclass
class LLMRequest:
    prompt: str
    model_id: str
    temperature: float = 0.7
    max_output_tokens: int = 1024
    stop_sequences: Optional[List[str]] = None
    system_instruction: Optional[str] = None

@dataclasses.dataclass
class LLMResponse:
    text: str
    raw_response: Dict[str, Any]

@dataclasses.dataclass
class ChatMessage:
    role: str
    parts: List[str]

@dataclasses.dataclass
class ChatRequest:
    messages: List[ChatMessage]
    model_id: str
    temperature: float = 0.7
    max_output_tokens: int = 1024
    stop_sequences: Optional[List[str]] = None
    system_instruction: Optional[str] = None
