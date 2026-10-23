import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embed a query and a list of document texts for semantic search.
    Returns a tuple (query_embedding, doc_embeddings).
    """
    client = get_embed_client()
    query_emb = client.embed(text=query)
    query_vec = normalize_embedding(query_emb.get('embedding', []))
    doc_embs = client.embed_batch(texts=documents)
    doc_vecs = [normalize_embedding(item.get('embedding', [])) for item in doc_embs]
    return query_vec, doc_vecs
