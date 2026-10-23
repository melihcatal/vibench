import os
from typing import TypedDict
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import ResponseShape, normalize_response


class GenerateEmbeddingResponse(TypedDict):
    embedding: list[float]

class GenerateBatchEmbeddingResponse(TypedDict):
    embeddings: list[list[float]]


def embed_for_search(query: str, documents: list[str], shape: ResponseShape = 'batch') -> tuple[GenerateEmbeddingResponse, list[GenerateEmbeddingResponse]]:
    """Embed a query and a collection of documents for semantic search.

    Args:
        query (str): The search query text.
        documents (list[str]): List of document texts to embed alongside the query.
        shape (ResponseShape, optional): 'single' for query only, 'batch' for query+documents together. Defaults to 'batch'.

    Returns:
        tuple[GenerateEmbeddingResponse, list[GenerateEmbeddingResponse]]: (query_embedding, [doc_embeddings...])
    """
    client = DirectEmbeddingsClient()
    if shape == 'single':
        query_resp = client.embed(text=query)
        query_norm = normalize_response(query_resp, 'single')
        query_vector = query_norm['embedding']
        # Embed batch for documents
        docs_resp = client.embed_batch(texts=documents)
        docs_norm = normalize_response(docs_resp, 'batch')
        doc_vectors = docs_norm['embeddings']
        return query_vector, doc_vectors
    else:
        # Embed both together in a single call (optional optimization)
        combined_resp = client.embed_batch(texts=[query] + documents)
        combined_norm = normalize_response(combined_resp, 'batch')
        query_vector = combined_norm['embeddings'][0]
        doc_vectors = combined_norm['embeddings'][1:]
        return query_vector, doc_vectors
