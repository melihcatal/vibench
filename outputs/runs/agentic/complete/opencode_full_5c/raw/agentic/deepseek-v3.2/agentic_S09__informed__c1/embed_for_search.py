import os
from typing import List, Tuple
from openai import OpenAI


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search using OpenAI Embeddings."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Embed query
    query_response = client.embeddings.create(
        model=model, input=query, encoding_format="float"
    )
    query_embedding = query_response.data[0].embedding

    # Embed documents
    docs_response = client.embeddings.create(
        model=model, input=documents, encoding_format="float"
    )
    document_embeddings = [item.embedding for item in docs_response.data]

    return query_embedding, document_embeddings
