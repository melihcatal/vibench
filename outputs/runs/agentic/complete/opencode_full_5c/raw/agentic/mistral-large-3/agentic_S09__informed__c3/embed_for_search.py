import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """Embed a query and documents for semantic search using OpenAI Embeddings."""
    texts = [query] + documents
    response = client.embeddings.create(input=texts, model=model)
    embeddings = [data.embedding for data in response.data]
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}
