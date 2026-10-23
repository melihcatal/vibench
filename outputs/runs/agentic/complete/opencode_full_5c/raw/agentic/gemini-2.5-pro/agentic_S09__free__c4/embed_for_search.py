from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import SearchEmbeddingResponse


def embed_for_search(query: str, documents: List[str]) -> SearchEmbeddingResponse:
    """
    Embeds a query and documents for semantic search using Cohere API.
    """
    cohere_client = get_cohere_client()
    model = "embed-english-v3.0"

    query_embedding = cohere_client.embed(
        texts=[query], model=model, input_type="search_query"
    ).embeddings[0]

    document_embeddings = cohere_client.embed(
        texts=documents, model=model, input_type="search_document"
    ).embeddings

    return SearchEmbeddingResponse(
        query_embedding=query_embedding,
        document_embeddings=document_embeddings,
        model=model,
    )
