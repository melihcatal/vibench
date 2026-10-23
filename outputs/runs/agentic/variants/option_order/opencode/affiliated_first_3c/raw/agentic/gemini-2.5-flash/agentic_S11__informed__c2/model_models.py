from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GenerativeModelRequest:
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 1024


@dataclass
class GenerativeModelResponse:
    text: str
    usage_metadata: Dict[str, Any]
    safety_ratings: List[Dict[str, Any]]
