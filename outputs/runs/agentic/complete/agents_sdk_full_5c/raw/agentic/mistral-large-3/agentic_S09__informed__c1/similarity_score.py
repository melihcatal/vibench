from typing import List
from embeddings_models import SimilarityScorer


def similarity_score(embedding_a: List[float], embedding_b: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    return SimilarityScorer.cosine_similarity(embedding_a, embedding_b)