from typing import List, Tuple
from embeddings_client import get_vertex_client
from embeddings_models import GOOGLE_EMBEDDING_MODEL

def embed_for_semantic_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    """
    Generates embeddings for a query and documents for semantic search.
    Uses specific task types for optimal performance with Google Vertex AI.

    Args:
        query: The search query.
        documents: A list of documents to be searched.

    Returns:
        A tuple containing the query embedding and a list of document embeddings.
    """
    client = get_vertex_client()

    # Embed the query with the 'RETRIEVAL_QUERY' task type
    query_embeddings = client.get_embeddings(
        [query], 
        model_name=GOOGLE_EMBEDDING_MODEL,
        task_type="RETRIEVAL_QUERY"
    )
    query_vector = query_embeddings[0].values

    # Embed the documents with the 'RETRIEVAL_DOCUMENT' task type
    doc_embeddings = client.get_embeddings(
        documents,
        model_name=GOOGLE_EMBEDDING_MODEL,
        task_type="RETRIEVAL_DOCUMENT"
    )
    doc_vectors = [embedding.values for embedding in doc_embeddings]

    return query_vector, doc_vectors
