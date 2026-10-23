from typing import List, Tuple
from embeddings_client import embed_single
from embeddings_models import l2_normalize, cosine_similarity

def embed_for_search(query: str, documents: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
    query_emb = l2_normalize(embed_single(model="text-embedding-3-small", query))
    doc_embs = [l2_normalize(embed_single(model="text-embedding-3-small", doc)) for doc in documents]
    similarities = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]
    scored_docs = list(zip(documents, similarities))
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return scored_docs[:top_k]
