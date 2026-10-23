# [SAME-SCENARIO] embed_for_search.py
# Embeds a query and a list of documents for semantic search

import os
from embeddings_client import get_openai_client
from embeddings_models import EmbedBatchRequest, EmbedBatchResponse
from similarity_score import cosine_similarity


def embed_for_search(query: str, documents: list[str]) -> dict:
    """Embed query and documents, then compute similarity scores.

    Returns a dict mapping each document to its similarity score with the query.
    """
    # Embed query
    query_resp = embed_text(query)  # reuse embed_text helper
    query_emb = query_resp.embedding

    # Embed documents in batch
    batch_resp = embed_batch(documents)  # reuse embed_batch helper
    doc_embs = batch_resp.embeddings

    # Compute similarities
    scores = {
        doc: cosine_similarity(query_emb, doc_emb)
        for doc, doc_emb in zip(documents, doc_embs)
    }
    return scores
