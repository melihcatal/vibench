from embeddings_client import cohere_client
from typing import List, Dict

def embed_query_and_documents(query: str, documents: List[str]) -> Dict:
    """
    Embeds a query and a list of documents for semantic search using Cohere.
    
    Args:
        query: The search query string.
        documents: A list of document strings.
        
    Returns:
        A dictionary with query and document embeddings.
    """
    # Embed the query with input_type='search_query'
    # Provider-specific model ID: embed-english-v3.0
    query_response = cohere_client.embed(
        texts=[query],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    query_embedding = query_response.embeddings[0]
    
    # Embed the documents with input_type='search_document'
    docs_response = cohere_client.embed(
        texts=documents,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    document_embeddings = docs_response.embeddings
    
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }
