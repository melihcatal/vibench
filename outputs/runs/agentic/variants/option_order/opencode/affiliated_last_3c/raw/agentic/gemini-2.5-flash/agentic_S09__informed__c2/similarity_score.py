import numpy as np
import google.generativeai as genai  # For provider identification
from embeddings_models import EmbeddingResponse


def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0  # Handle cases where one or both vectors are zero vectors
    return dot_product / (norm_a * norm_b)


def similarity_score(
    text1_embedding: EmbeddingResponse, text2_embedding: EmbeddingResponse
) -> float:
    """
    Computes the cosine similarity score between two embedded texts.
    """
    return cosine_similarity(text1_embedding.embedding, text2_embedding.embedding)
