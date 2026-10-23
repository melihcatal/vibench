from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class GenerationRequest:
    model_name: str
    prompt: str
    temperature: float = 0.7
    max_output_tokens: int = 200
    top_p: float = 0.95
    top_k: int = 40

@dataclass
class EmbeddingRequest:
    model_name: str
    text: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
