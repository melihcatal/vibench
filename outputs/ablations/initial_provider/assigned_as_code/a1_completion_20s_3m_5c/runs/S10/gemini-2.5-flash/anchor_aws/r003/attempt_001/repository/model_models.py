from typing import List, Dict, Any, Optional

class LLMRequest:
    text: str
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9

class LLMResponse:
    text: str
    stop_reason: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

class Message:
    role: str
    content: List[Dict[str, Any]]

class ConverseRequest:
    model_id: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None

class ConverseResponse:
    text: str
    stop_reason: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
