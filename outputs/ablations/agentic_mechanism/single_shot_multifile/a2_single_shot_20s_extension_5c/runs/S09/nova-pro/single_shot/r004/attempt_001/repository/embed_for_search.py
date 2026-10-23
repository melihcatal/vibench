import os
from embeddings_client import get_embeddings_client

def embed_for_search(query, documents):
    client = get_embeddings_client()
    query_embedding = client.embed_text(query)
    document_embeddings = client.embed_batch(documents)
    return query_embedding, document_embeddings