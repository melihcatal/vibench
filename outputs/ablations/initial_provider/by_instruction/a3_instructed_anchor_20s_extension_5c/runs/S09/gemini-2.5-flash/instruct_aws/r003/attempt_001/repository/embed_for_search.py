from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResult

def embed_for_search(query: str, documents: List[str]) -> tuple[EmbeddingResult, List[EmbeddingResult]]:
    """Embeds a query and a list of documents for semantic search using AWS Bedrock.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing:
            - An EmbeddingResult object for the query.
            - A list of EmbeddingResult objects for the documents.
    """
    client = EmbeddingsClient()
    query_embedding = client.get_embedding(query)
    query_result = EmbeddingResult(embedding=query_embedding, text=query)

    document_embeddings_data = client.get_batch_embeddings(documents)
    document_results = []
    for i, embedding in enumerate(document_embeddings_data):
        document_results.append(EmbeddingResult(embedding=embedding, text=documents[i]))

    return query_result, document_results
