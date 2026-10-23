def normalize_embedding(embedding):
    from numpy.linalg import norm
    return embedding / norm(embedding)