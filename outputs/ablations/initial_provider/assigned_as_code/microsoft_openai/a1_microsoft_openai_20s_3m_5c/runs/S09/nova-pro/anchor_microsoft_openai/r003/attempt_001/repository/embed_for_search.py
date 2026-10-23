import os
from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse
from embeddings_client import get_embeddings_client


def embed_for_search(query, documents, config=None):
    client = get_embeddings_client(config)
    query_request = EmbeddingRequest(texts=[query])
    document_request = EmbeddingRequest(texts=documents)
    query_response = client.embeddings.create(model='text-embedding-3-small', input=query_request.texts)
    document_response = client.embeddings.create(model='text-embedding-3-small', input=document_request.texts)
    return EmbeddingResponse(query_embedding=query_response.data[0].embedding, document_embeddings=[item.embedding for item in document_response.data])