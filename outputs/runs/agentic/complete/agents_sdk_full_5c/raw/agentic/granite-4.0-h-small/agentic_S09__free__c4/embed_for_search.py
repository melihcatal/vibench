# embed_for_search.py
import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> dict:
    """Embed a query and a list of documents for semantic search.",
    client = DirectEmbeddingsClient()
    query_emb = client.embed(text=query)
    # Assume response contains a key "embedding"
    query_vec = normalize_embedding(query_emb["embedding"])
    doc_vecs = [normalize_embedding(client.embed(text=doc)["embedding"]) for doc in documents]
    return {
        "query_vector": query_vec,
        "document_vectors": doc_vecs,
    }