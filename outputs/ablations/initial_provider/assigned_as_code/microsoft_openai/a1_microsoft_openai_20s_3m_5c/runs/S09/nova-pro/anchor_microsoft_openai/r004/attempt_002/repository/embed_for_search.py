import os
from openai import OpenAI

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_for_search(query, documents, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    query_embedding = client.embeddings.create(model='text-embedding-3-small', input=query)
    document_embeddings = client.embeddings.create(model='text-embedding-3-small', input=documents)
    query_embedding = normalize_embedding_response(query_embedding.data[0])
    document_embeddings = [normalize_embedding_response(embedding) for embedding in document_embeddings.data]
    return {'query_embedding': query_embedding, 'document_embeddings': document_embeddings}