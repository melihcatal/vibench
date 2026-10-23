import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of documents, returning similarity scores."""
    client = DirectEmbeddingsClient()
    query_vec = client.embed(text=query)
    query_vec = normalize_embedding(query_vec.get('embedding'))
    doc_vectors = []
    for doc in documents:
        vec = client.embed(text=doc)
        doc_vectors.append((doc, normalize_embedding(vec.get('embedding'))))
    # Compute cosine similarities
    similarities = []
    for doc, vec in doc_vectors:
        sim = cosine_similarity(query_vec, vec)
        similarities.append((doc, sim))
    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities
