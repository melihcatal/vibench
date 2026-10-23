from typing import List, Any

Embedding = List[float]
BatchEmbeddings = List[Embedding]


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    if len(emb1) != len(emb2):
        raise ValueError("Embeddings must have the same dimension")
    dot_product = sum(x * y for x, y in zip(emb1, emb2))
    norm1 = (sum(x * x for x in emb1)) ** 0.5
    norm2 = (sum(x * x for x in emb2)) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def normalize_embedding(emb: List[Any]) -> Embedding:
    return [float(x) for x in emb]
