from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LLMTextRequest:
    """Represents a request for text generation from an LLM."""
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 256
    top_p: float = 0.95
    top_k: int = 40

@dataclass
class LLMTextResponse:
    """Represents a response from an LLM text generation."""
    text: str
    safety_attributes: Optional[dict] = field(default_factory=dict)
    citation_metadata: Optional[dict] = field(default_factory=dict)

