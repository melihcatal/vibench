# [SAME-SCENARIO] embed_for_search.py
# Embeds a query and a list of documents for semantic search

# Provider: OpenAI Embeddings
# SDK: openai
# Integration signal: OPENAI_API_KEY environment variable

import os
from typing import List
from openai import OpenAI
from .embed_text import embed_text

embeddings_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_for_search(
    query: str, documents: List[str]
) -> tuple[list[float], List[list[float]]]:
    """Embed query and each document.
    Returns a tuple (query_embedding, list_of_document_embeddings).
    """
    query_embedding = embed_text(query)
    doc_embeddings = [embed_text(doc) for doc in documents]
    return query_embedding, doc_embeddings
