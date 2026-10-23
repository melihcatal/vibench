from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ModelResponse:
    """
    A simple data class to structure responses from the LLM service.
    """
    id: str
    text: str
    finish_reason: Optional[str] = None

@dataclass
class ModelRequest:
    """
    A simple data class to structure requests to the LLM service.
    """
    prompt: str
    model: str
    max_tokens: int = 1024
    stream: bool = False
