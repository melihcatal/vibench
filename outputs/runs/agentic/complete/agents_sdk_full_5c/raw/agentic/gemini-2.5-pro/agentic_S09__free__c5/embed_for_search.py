from typing import List, Tuple
from embeddings_client import get_embeddings_client

def embed_query_and_documents(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """
    Generates embeddings for a query and a list of documents for semantic search.
    It uses specific task types for query and document as recommended by Google Vertex AI.

    Args:
        query: The search query.
        documents: A list of documents to be searched.

    Returns:
        A tuple containing the query embedding and a list of document embeddings.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    if not documents or not isinstance(documents, list):
        raise ValueError("Documents must be a non-empty list of strings.")

    client = get_embeddings_client()

    # Embed the query with the 'RETRIEVAL_QUERY' task type
    query_embedding_list = client.get_embeddings(
        [query], task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_embedding_list[0].values

    # Embed the documents with the 'RETRIEVAL_DOCUMENT' task type
    doc_embeddings_list = client.get_embeddings(
        documents, task_type="RETRIEVAL_DOCUMENT"
    )
    doc_embeddings = [embedding.values for embedding in doc_embeddings_list]

    return query_embedding, doc_embeddings
