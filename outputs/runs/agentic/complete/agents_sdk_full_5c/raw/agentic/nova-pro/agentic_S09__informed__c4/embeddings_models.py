def normalize_embedding(embedding):
    from numpy.linalg import norm
    norm_embedding = embedding / norm(embedding)
    return norm_embedding.tolist()