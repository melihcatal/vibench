from embeddings_client import cohere_client
from typing import List, Dict

MODEL_NAME = "embed-english-v3.0"

def embed_query_and_documents(query: str, documents: List[str]) -> Dict[str, List]:
    """
    Embeds a query and a list of documents for semantic search.
    Uses different input types for query and documents as recommended by Cohere.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    if not documents or not isinstance(documents, list):
        raise ValueError("Documents must be a non-empty list of strings.")

    # Embed the query
    query_response = cohere_client.embed(
        texts=[query],
        model=MODEL_NAME,
        input_type="search_query"
    )
    query_embedding = query_response.embeddings[0]

    # Embed the documents
    docs_response = cohere_client.embed(
        texts=documents,
        model=MODEL_NAME,
        input_type="search_document"
    )
    doc_embeddings = docs_response.embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings
    }
