import os
from typing import List, Tuple
import openai
from embeddings_client import get_embeddings_client


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search using OpenAI Embeddings."""
    client = get_embeddings_client()

    all_texts = [query] + documents

    response = client.embeddings.create(
        model=model, input=all_texts, encoding_format="float"
    )

    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]

    return query_embedding, document_embeddings
