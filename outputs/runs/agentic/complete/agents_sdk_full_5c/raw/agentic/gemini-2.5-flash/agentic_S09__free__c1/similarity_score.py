import numpy as np

def similarity_score(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedded texts.

    Args:
        embedding1: The first embedding vector (e.g., from Vertex AI textembedding-gecko@003).
        embedding2: The second embedding vector (e.g., from Vertex AI textembedding-gecko@003).

    Returns:
        The cosine similarity score between the two embeddings.
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
    # Example usage (assuming embeddings are from a provider like Vertex AI):
    # embedding_a = [0.1, 0.2, 0.3]
    # embedding_b = [0.15, 0.25, 0.35]
    # embedding_c = [0.9, 0.8, 0.7]
    # score_ab = similarity_score(embedding_a, embedding_b)
    # score_ac = similarity_score(embedding_a, embedding_c)
    # print(f"Similarity (A, B): {score_ab}")
    # print(f"Similarity (A, C): {score_ac}")
    pass
