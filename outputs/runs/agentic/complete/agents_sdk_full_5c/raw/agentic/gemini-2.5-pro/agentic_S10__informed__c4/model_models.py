from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CompletionRequest:
    """
    A simplified request structure for model completion.
    """
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 150

@dataclass
class CompletionResponse:
    """
    A simplified response structure from a model completion.
    """
    text: str
    finish_reason: Optional[str] = None
    token_usage: Optional[dict] = None
