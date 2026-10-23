from typing import List, Tuple
from embeddings_client import cohere_client


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """
    Embeds a query and documents for semantic search using Cohere.
    """
    query_embedding_response = cohere_client.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )
    query_embedding = query_embedding_response.embeddings[0]

    document_embeddings_response = cohere_client.embed(
        texts=documents, model="embed-english-v3.0", input_type="search_document"
    )
    document_embeddings = document_embeddings_response.embeddings

    return query_embedding, document_embeddings
