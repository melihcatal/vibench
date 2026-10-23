from typing import List, Any


def parse_embeddings(response: Any) -> List[List[float]]:
    """Parse OpenAI embeddings API response."""
    return [item["embedding"] for item in response.data]


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    """Cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = sum(a * a for a in emb1) ** 0.5
    norm2 = sum(b * b for b in emb2) ** 0.5
    return dot_product / (norm1 * norm2 + 1e-8)
