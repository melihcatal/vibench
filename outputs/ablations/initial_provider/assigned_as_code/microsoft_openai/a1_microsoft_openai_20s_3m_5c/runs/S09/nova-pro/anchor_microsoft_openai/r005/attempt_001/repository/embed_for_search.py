import os
from openai import OpenAI

from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_for_search(payload, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    query_response = client.embeddings.create(model='text-embedding-3-small', input=payload['query'])
    document_responses = client.embeddings.create(model='text-embedding-3-small', input=payload['documents'])
    query_embedding = normalize_embedding_response(query_response.data[0])
    document_embeddings = [normalize_embedding_response(doc) for doc in document_responses.data]
    return {'query_embedding': query_embedding, 'document_embeddings': document_embeddings}