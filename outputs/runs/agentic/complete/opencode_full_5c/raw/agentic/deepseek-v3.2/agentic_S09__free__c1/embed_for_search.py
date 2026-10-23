import os
from typing import List, Tuple
from openai import OpenAI


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """
    Embed a query and documents for semantic search using OpenAI's embeddings API.

    Args:
        query: The search query text
        documents: List of document texts to search against
        model: The OpenAI embedding model to use (default: text-embedding-3-small)

    Returns:
        Tuple of (query_embedding, document_embeddings)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    all_texts = [query] + documents

    response = client.embeddings.create(
        model=model, input=all_texts, encoding_format="float"
    )

    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]

    return query_embedding, document_embeddings
