from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Embedding request model."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    """Embedding response model."""

    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """Normalize embeddings to unit vectors."""
    normalized = []
    for emb in embeddings:
        vec = np.array(emb)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        normalized.append(vec.tolist())
    return normalized


def parse_openai_response(response) -> EmbeddingResponse:
    """Parse OpenAI embedding response."""
    embeddings = [item.embedding for item in response.data]
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return EmbeddingResponse(embeddings=embeddings, model=response.model, usage=usage)


def create_batch_requests(texts: List[str], batch_size: int = 100) -> List[List[str]]:
    """Create batches of texts for embedding."""
    batches = []
    for i in range(0, len(texts), batch_size):
        batches.append(texts[i : i + batch_size])
    return batches
