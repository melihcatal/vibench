from dataclasses import dataclass, field
from typing import List, Dict, Any, Generator


@dataclass
class Message:
    role: str
    content: str


@dataclass
class GenerationRequest:
    messages: List[Message]
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclass
class GenerationMetadata:
    prompt_token_count: int = 0
    candidates_token_count: int = 0
    total_token_count: int = 0


@dataclass
class GenerationResponse:
    content: str = ""
    metadata: GenerationMetadata = field(default_factory=GenerationMetadata)
