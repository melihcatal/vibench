# embed_for_search.py - SAME-SCENARIO
# Embeds a query and a list of documents for semantic search

import os
import dashscope
from typing import List

# Load API key from environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("Set DASHSCOPE_API_KEY environment variable")

dashscope.api_key = DASHSCOPE_API_KEY


def embed_for_search(query: str, documents: List[str]) -> dict:
    """Embed a query and a list of documents, returning a combined result.

    Args:
        query (str): The search query.
        documents (list of str): Texts to embed for retrieval.

    Returns:
        dict: Mapping of 'query' and each document index to its embedding vector.
    """
    response = dashscope.embeddings.create(
        model="text-embedding-003",  # concrete model identifier
        texts=[query] + documents,
    )
    embeddings = response["embeddings"]
    result = {
        "query": embeddings[0]["data"],
    }
    for idx, doc_emb in enumerate(embeddings[1:], start=1):
        result[f"doc_{idx}"] = doc_emb["data"]
    return result
