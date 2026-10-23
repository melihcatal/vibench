from typing import List
import math
from embeddings_client import embed_texts
from embeddings_models import normalize_texts


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(emb1) != len(emb2):
        raise ValueError("Embeddings must have the same dimension")
    dot_product = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = math.sqrt(sum(a * a for a in emb1))
    norm2 = math.sqrt(sum(b * b for b in emb2))
    return dot_product / (norm1 * norm2)


def similarity_score(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two embedded texts using OpenAI text-embedding-3-small.
    """
    normalized_texts = normalize_texts([text1, text2])
    embeddings = embed_texts(normalized_texts)
    return cosine_similarity(embeddings[0], embeddings[1])
