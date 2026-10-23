from typing import List, Tuple
import math
from embeddings_client import get_embeddings_client, create_embedding
from embeddings_models import parse_embeddings_response

MODEL = "text-embedding-3-small"


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = math.sqrt(sum(a * a for a in emb1))
    norm2 = math.sqrt(sum(b * b for b in emb2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def embed_for_search(query: str, documents: List[str]) -> List[Tuple[str, float]]:
    client = get_embeddings_client()
    all_texts = [query] + documents
    response = create_embedding(client, MODEL, all_texts)
    embs = parse_embeddings_response(response)
    query_emb = embs[0]
    results = []
    for doc_emb, doc in zip(embs[1:], documents):
        sim = cosine_similarity(query_emb, doc_emb)
        results.append((doc, sim))
    return sorted(results, key=lambda x: x[1], reverse=True)
