from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EmbeddingsRequest:
    texts: List[str]

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class BatchEmbeddingsResponse:
    embeddings: List[List[float]]

def normalize_embedding_response(genai_response: Any) -> EmbeddingResponse:
    """Normalizes the genai client's embedding response."""
    # Assuming genai_response.embeddings[0].values is the structure for single embedding
    return EmbeddingResponse(embedding=list(genai_response.embeddings[0].values))

def normalize_batch_embedding_response(genai_response: Any) -> BatchEmbeddingsResponse:
    """Normalizes the genai client's batch embedding response."""
    # Assuming genai_response.embeddings is a list of embedding objects
    return BatchEmbeddingsResponse(embeddings=[list(e.values) for e in genai_response.embeddings])
