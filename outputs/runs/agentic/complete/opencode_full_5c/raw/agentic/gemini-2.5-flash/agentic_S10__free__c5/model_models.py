from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class LLMRequest:
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1024
    model_name: str = "gemini-pro"  # Default model for general use


@dataclass
class LLMResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class SafetyRating:
    category: str
    probability: str


@dataclass
class SafetyResult:
    blocked: bool
    safety_ratings: List[SafetyRating]
