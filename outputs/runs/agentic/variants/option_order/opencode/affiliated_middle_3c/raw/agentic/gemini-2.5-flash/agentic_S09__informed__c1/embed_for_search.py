from embeddings_client import get_gemini_embeddings_client


def embed_for_search(
    query: str, documents: list[str], model_name: str = "models/embedding-001"
) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.

    Args:
        query: The query string to embed.
        documents: A list of document strings to embed.
        model_name: The name of the embedding model to use. Default is "models/embedding-001".

    Returns:
        A tuple containing:
        - The embedding vector for the query (list of floats).
        - A list of embedding vectors for the documents (list of lists of floats).
    """
    genai = get_gemini_embeddings_client()

    query_embedding_response = genai.embed_content(
        model=model_name, content=query, task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_embedding_response["embedding"]

    document_embeddings_response = genai.embed_content(
        model=model_name, content=documents, task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [
        item["embedding"] for item in document_embeddings_response["embeddings"]
    ]

    return query_embedding, document_embeddings
