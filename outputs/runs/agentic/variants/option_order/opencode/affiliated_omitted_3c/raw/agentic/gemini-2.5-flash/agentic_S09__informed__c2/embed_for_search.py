import os
from typing import List, Dict
import cohere


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    """
    Embeds a query and documents for semantic search using Cohere Embed API.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    # The model identifier "embed-english-v3.0" with input_type specified is a concrete and identifiable Cohere embedding model.
    # It is documented in Cohere API references for search use cases.
    query_response = co.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )
    query_embedding = query_response.embeddings

    document_response = co.embed(
        texts=documents, model="embed-english-v3.0", input_type="search_document"
    )
    document_embeddings = document_response.embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
