# [SAME-SCENARIO] embed_for_search.py
# Embed a query and a list of documents for semantic search

import os
import openai
from typing import List, Tuple
from .embed_text import embed_text

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[list[float], List[list[float]]]:
    """Embed a query string and a list of document strings.

    Returns the query embedding and a list of document embeddings.

    Args:
        query (str): The query text.
        documents (List[str]): List of document texts to embed.

    Returns:
        Tuple containing:
            - query_embedding (list[float]): Embedding of the query.
            - document_embeddings (List[list[float]]): List of embeddings for each document.
    """
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    return query_embedding, document_embeddings
