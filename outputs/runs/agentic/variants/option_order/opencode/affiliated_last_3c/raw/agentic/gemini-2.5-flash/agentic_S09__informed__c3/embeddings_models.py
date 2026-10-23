import numpy as np

EMBEDDING_MODEL = "models/embedding-001"


def normalize_embedding(embedding):
    """Normalizes an embedding vector."""
    return embedding / np.linalg.norm(embedding)


def cosine_similarity(embedding1, embedding2):
    """Computes the cosine similarity between two embedding vectors."""
    embedding1_norm = normalize_embedding(np.array(embedding1))
    embedding2_norm = normalize_embedding(np.array(embedding2))
    return np.dot(embedding1_norm, embedding2_norm)
