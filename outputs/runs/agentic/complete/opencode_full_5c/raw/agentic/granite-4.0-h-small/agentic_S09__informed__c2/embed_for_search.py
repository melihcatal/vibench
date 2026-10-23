import os
from dashscope import embeddings  # DashScope Embeddings SDK
from typing import List


def embed_for_search(query: str, documents: List[str]):
    """Embed a query and a list of documents for semantic search.

    Uses DashScope to embed the query and each document.

    Args:
        query (str): The search query.
        documents (List[str]): Collection of document texts.

    Returns:
        dict: A dictionary with keys 'query_embedding' and 'doc_embeddings'.
    """
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    # Embed query
    query_resp = embeddings.embed(texts=[query])
    query_embedding = query_resp[0]["embedding"]
    # Embed documents
    doc_resp = embeddings.embed(texts=documents)
    doc_embeddings = [entry["embedding"] for entry in doc_resp]
    return {"query_embedding": query_embedding, "doc_embeddings": doc_embeddings}
