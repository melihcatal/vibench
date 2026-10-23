import numpy as np

def similarity_score(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity score between the two vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == '__main__':
    # Example usage with dummy embeddings (e.g., from Vertex AI textembedding-gecko output)
    # These are NOT actual embeddings, just for demonstration of similarity calculation.
    embedding_a = [0.1, 0.2, 0.3]
    embedding_b = [0.1, 0.2, 0.3]
    embedding_c = [0.4, 0.5, 0.6]

    # print(f"Similarity between A and B: {similarity_score(embedding_a, embedding_b)}") # Expected: ~1.0
    # print(f"Similarity between A and C: {similarity_score(embedding_a, embedding_c)}") # Expected: < 1.0
    pass
