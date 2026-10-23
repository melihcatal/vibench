from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class LLMRequest:
    """Represents a generic request to an LLM."""
    prompt: str
    model_id: str = "gemini-pro"
    temperature: float = 0.7
    max_tokens: int = 1024
    stop_sequences: Optional[List[str]] = None
    stream: bool = False

@dataclass
class LLMResponse:
    """Represents a generic response from an LLM."""
    generated_text: str
    model_id: str = "gemini-pro"
    raw_response: Any = field(repr=False) # Store the raw response object if needed

@dataclass
class LLMStreamChunk:
    """Represents a chunk of a streaming LLM response."""
    text_chunk: str
    finish_reason: Optional[str] = None
