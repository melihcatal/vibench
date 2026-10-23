from typing import List
from math import sqrt
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_texts


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(vec1, vec2))
    norm1 = sqrt(sum(x * x for x in vec1))
    norm2 = sqrt(sum(y * y for y in vec2))
    return dot_product / (norm1 * norm2) if norm1 * norm2 != 0 else 0.0


def similarity_score(text1: str, text2: str) -> float:
    client = get_embeddings_client()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_texts([text1, text2])
    )
    emb1 = [float(x) for x in response.data[0].embedding]
    emb2 = [float(x) for x in response.data[1].embedding]
    return cosine_similarity(emb1, emb2)
