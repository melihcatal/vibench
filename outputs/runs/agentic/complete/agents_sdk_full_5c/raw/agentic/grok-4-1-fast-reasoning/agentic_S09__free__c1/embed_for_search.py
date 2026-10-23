from typing import List, Tuple
from embeddings_client import get_embedding, get_embeddings
from embeddings_models import normalize_embedding, cosine_similarity

def embed_for_search(query: str, documents: List[str]) -> List[Tuple[str, float]]:
    query_emb = normalize_embedding(get_embedding(query, model="text-embedding-3-small"))
    doc_embs = [normalize_embedding(e) for e in get_embeddings(documents, model="text-embedding-3-small")]
    scores = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]
    return list(zip(documents, scores))
