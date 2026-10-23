from typing import List, Dict, Union
from embeddings_client import get_embeddings_client

def embed_for_semantic_search(query: str, documents: List[str]) -> Dict[str, Union[List[float], List[List[float]]]]:
    """
    Generates embeddings for a query and a list of documents,
    optimized for semantic search, using the Cohere API.

    Args:
        query: The search query string.
        documents: A list of document strings.

    Returns:
        A dictionary containing the query embedding and a list of document embeddings.
    """
    client = get_embeddings_client()
    
    # Use a specific Cohere model for embeddings
    model = "embed-english-v3.0"
    
    # Embed the query with input_type 'search_query'
    query_response = client.embed(
        texts=[query],
        model=model,
        input_type="search_query"
    )
    query_embedding = query_response.embeddings[0]
    
    # Embed the documents with input_type 'search_document'
    # This is crucial for models that distinguish between query and document embeddings.
    docs_response = client.embed(
        texts=documents,
        model=model,
        input_type="search_document"
    )
    doc_embeddings = docs_response.embeddings
    
    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings
    }

