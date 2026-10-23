from typing import List, Tuple

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, BatchEmbeddingRequest, EmbeddingResponse, BatchEmbeddingResponse, normalize_text

def embed_for_search(
    query_text: str,
    document_texts: List[str],
    model: str = "text-embedding-ada-002"
) -> Tuple[EmbeddingResponse, BatchEmbeddingResponse]:
    """Embeds a query and a list of documents for semantic search using OpenAI.

    Args:
        query_text: The query string.
        document_texts: A list of document strings.
        model: The OpenAI embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        A tuple containing the EmbeddingResponse for the query and
        a BatchEmbeddingResponse for the documents.
    """
    client = EmbeddingsClient()

    normalized_query = normalize_text(query_text)
    query_request = EmbeddingRequest(text=normalized_query, model=model)
    query_embedding_response = client.get_embedding(query_request)

    normalized_documents = [normalize_text(text) for text in document_texts]
    documents_request = BatchEmbeddingRequest(texts=normalized_documents, model=model)
    documents_embedding_response = client.get_batch_embeddings(documents_request)

    return query_embedding_response, documents_embedding_response
