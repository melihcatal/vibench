import numpy as np


def normalize_embedding(embedding):
    """Normalizes an embedding vector."""
    return np.array(embedding) / np.linalg.norm(embedding)


def calculate_cosine_similarity(embedding1, embedding2):
    """Calculates the cosine similarity between two embedding vectors."""
    emb1_np = np.array(embedding1)
    emb2_np = np.array(embedding2)
    dot_product = np.dot(emb1_np, emb2_np)
    norm_a = np.linalg.norm(emb1_np)
    norm_b = np.linalg.norm(emb2_np)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
