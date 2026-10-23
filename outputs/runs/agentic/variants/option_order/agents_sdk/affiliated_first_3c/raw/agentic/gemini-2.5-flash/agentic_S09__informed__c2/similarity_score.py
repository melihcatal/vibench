import numpy as np

def similarity_score(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0 # Handle zero vectors gracefully

    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == '__main__':
    # Example usage - embeddings would typically come from an embedding API
    # Example dummy embeddings for demonstration
    # embedding_a = [0.1, 0.2, 0.3, 0.4, 0.5]
    # embedding_b = [0.1, 0.2, 0.3, 0.4, 0.5] # Identical
    # embedding_c = [0.5, 0.4, 0.3, 0.2, 0.1] # Different but similar magnitude
    # embedding_d = [-0.1, -0.2, -0.3, -0.4, -0.5] # Opposite direction

    # score_ab = similarity_score(embedding_a, embedding_b)
    # score_ac = similarity_score(embedding_a, embedding_c)
    # score_ad = similarity_score(embedding_a, embedding_d)

    # print(f"Similarity (A, B): {score_ab}") # Expected ~1.0
    # print(f"Similarity (A, C): {score_ac}") # Expected positive, less than 1.0
    # print(f"Similarity (A, D): {score_ad}") # Expected ~-1.0
    pass
