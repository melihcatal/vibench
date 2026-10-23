from typing import List, Tuple
from math import sqrt
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_texts


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(vec1, vec2))
    norm1 = sqrt(sum(x * x for x in vec1))
    norm2 = sqrt(sum(y * y for y in vec2))
    return dot_product / (norm1 * norm2) if norm1 * norm2 != 0 else 0.0


def embed_for_search(
    query: str, documents: List[str], top_k: int = 5
) -> List[Tuple[str, float]]:
    client = get_embeddings_client()
    all_texts = normalize_texts([query] + documents)
    response = client.embeddings.create(model="text-embedding-3-small", input=all_texts)
    query_emb = [float(x) for x in response.data[0].embedding]
    doc_embs = [[float(x) for x in emb.embedding] for emb in response.data[1:]]
    similarities = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]
    results = list(zip(documents, similarities))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]
