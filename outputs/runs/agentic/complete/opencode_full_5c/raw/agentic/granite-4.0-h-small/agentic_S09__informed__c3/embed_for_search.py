# [SAME-SCENARIO] embed_for_search.py
# Embed a query and a collection of documents for semantic search

# Identifiable provider: OpenAI (OpenAI Embeddings) used for both query and documents
import os
import openai
from typing import List, Tuple

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[list[float], List[list[float]]]:
    """
    Return a tuple of:
    - embedding vector for the query (list[float])
    - list of embedding vectors for each document (List[list[float]])

    Uses OpenAI's text-embedding-ada-002 model via the OpenAI SDK.
    """
    # Embed query
    query_resp = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=query,
    )
    query_embedding = query_resp["data"][0]["embedding"]

    # Embed documents in batch
    docs_resp = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=documents,
    )
    docs_embeddings = [item["embedding"] for item in docs_resp["data"]]

    return query_embedding, docs_embeddings
