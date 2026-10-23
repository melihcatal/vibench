from embeddings_client import embed_single, embed_batch, normalize_embedding
from embeddings_models import cosine_similarity
from typing import List, Tuple


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]], List[float]]:
    q_emb = normalize_embedding(embed_single(query, input_type="search_query"))
    doc_embs_raw = embed_batch(documents, input_type="search_document")
    doc_embs = [normalize_embedding(e) for e in doc_embs_raw]
    similarities = [cosine_similarity(q_emb, de) for de in doc_embs]
    return q_emb, doc_embs, similarities
