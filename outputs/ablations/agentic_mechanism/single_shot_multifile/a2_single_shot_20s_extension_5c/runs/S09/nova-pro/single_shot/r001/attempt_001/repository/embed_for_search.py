import os
from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def embed_for_search(query, documents):
    query_embedding = client.generate_embedding(query)
    document_embeddings = client.generate_batch_embeddings(documents)
    return query_embedding, document_embeddings