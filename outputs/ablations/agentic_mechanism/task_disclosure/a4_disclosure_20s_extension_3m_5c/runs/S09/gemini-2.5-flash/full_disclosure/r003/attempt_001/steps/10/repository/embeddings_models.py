import dataclasses
from typing import List, Dict

@dataclasses.dataclass
class EmbeddingRequest:
    texts: List[str]
    model_id: str = "text-embedding-004" # Default model for Direct Embeddings API

@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]] # List of embedding vectors

def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector."""
    if not embedding:
        return []
    
    magnitude = sum(x**2 for x in embedding)**0.5
    if magnitude == 0:
        return embedding # Avoid division by zero
    
    return [x / magnitude for x in embedding]
