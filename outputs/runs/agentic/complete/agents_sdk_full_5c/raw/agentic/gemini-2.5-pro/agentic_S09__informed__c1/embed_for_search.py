from typing import List, Dict
from embeddings_client import get_cohere_client

# Note: Using a specific model version is a best practice.
COHERE_MODEL_NAME = "embed-english-v3.0"

def embed_for_search(query: str, documents: List[str]) -> Dict:
    """
    Embeds a query and a list of documents for semantic search using Cohere.
    This uses different input types for query and documents as recommended by Cohere.

    Args:
        query: The search query string.
        documents: A list of document strings.

    Returns:
        A dictionary with 'query_embedding' and 'document_embeddings'.
    """
    client = get_cohere_client()

    # Embed the query with 'search_query' input type
    query_response = client.embed(
        texts=[query],
        model=COHERE_MODEL_NAME,
        input_type="search_query"
    )
    query_embedding = query_response.embeddings[0]

    # Embed the documents with 'search_document' input type
    doc_response = client.embed(
        texts=documents,
        model=COHERE_MODEL_NAME,
        input_type="search_document"
    )
    document_embeddings = doc_response.embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }
