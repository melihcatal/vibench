from dataclasses import dataclass
from typing import List

@dataclass
class EmbeddingResponse:
    """Represents the response structure for a text embedding."""
    text: str
    embedding: List[float]
    model: str

@dataclass
class EmbeddingJobResult:
    """Represents a single result from an embedding job, including source text and its embedding."""
    id: str
    source_text: str
    embedding: List[float]
    model_used: str