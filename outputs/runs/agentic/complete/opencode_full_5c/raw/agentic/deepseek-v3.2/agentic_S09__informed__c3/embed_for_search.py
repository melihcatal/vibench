import os
from openai import OpenAI
from typing import List, Tuple


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search using OpenAI Embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Embed query
    query_response = client.embeddings.create(
        model=model, input=query, encoding_format="float"
    )
    query_embedding = query_response.data[0].embedding

    # Embed documents
    doc_response = client.embeddings.create(
        model=model, input=documents, encoding_format="float"
    )
    doc_embeddings = [item.embedding for item in doc_response.data]

    return query_embedding, doc_embeddings
