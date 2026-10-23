class EmbeddingRequest:
    def __init__(self, text):
        self.text = text


class EmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding


def normalize_embedding(embedding):
    import numpy as np

    return np.array(embedding) / np.linalg.norm(embedding)
