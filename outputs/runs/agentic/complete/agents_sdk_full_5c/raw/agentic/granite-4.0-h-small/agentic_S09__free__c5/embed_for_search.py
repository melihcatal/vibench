import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> list[float]:
    """Embed a search query and a list of document texts, returning cosine similarity scores.
    """
    client = get_client()
    # Embed query
    query_emb = get_client().create(
        model="text-embedding-ada-002",
        input=query,
        dimensions=1536,
    )['embedding']
    query_emb = normalize_embedding(query_emb)

    # Embed documents
    docs_response = client.create(
        model="text-embedding-ada-002",
        input=documents,
        dimensions=1536,
    )
    doc_embs = [normalize_embedding(emb['embedding']) for emb in docs_response.get('embeddings', [])]

    # Compute similarities
    similarities = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embs]
    return similarities
