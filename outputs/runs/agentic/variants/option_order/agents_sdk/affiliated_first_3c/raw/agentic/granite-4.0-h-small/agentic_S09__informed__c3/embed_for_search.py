import os
from embeddings_client import get_embed_client

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embed a query and a list of document texts for semantic search.\n\n    Returns a tuple (query_embedding, doc_embeddings).\n    """
    client = get_embed_client()
    query_embedding = client.embed(text=query)['embedding']
    doc_embeddings = [client.embed(text=d)['embedding'] for d in documents]
    return query_embedding, doc_embeddings