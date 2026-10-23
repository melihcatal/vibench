from __future__ import annotations

import os
from typing import List

from embeddings_client import create_client
from embeddings_models import BatchEmbedRequest, resolve_model_id
from similarity_score import batch_similarity


def _prepare_payload(texts: List[str], model_id: str) -> dict:
    """Create IBM Watsonx embeddings API payload from generic request data.","""
    return {"input": texts, "model": model_id}


def embed_for_search(
    query: str, corpus_documents: List[str], model_id: str = "embed-ada-002"
) -> List[float]:
    """Generate embeddings for a query and a corpus batch, then compute similarity.","""
    model_id = resolve_model_id(model_id)
    client = create_client()
    # 1. embed query
    payload_q = _prepare_payload([query], model_id=model_id)
    response_q = client.create_embeddings(payload_q)  # type: ignore
    query_vec = (
        response_q[0] if isinstance(response_q, list) else response_q["embeddings"][0]
    )
    # 2. embed corpus batch
    payload_corpus = _prepare_payload(corpus_documents, model_id=model_id)
    response_corpus = client.create_embeddings(payload_corpus)  # type: ignore
    corpus_vecs = (
        [doc["embeddings"][0] for doc in response_corpus]
        if isinstance(response_corpus, list)
        else response_corpus["embeddings"]
    )
    # 3. compute similarity (simplest: max similarity per query)
    sims = batch_similarity([query_vec], corpus_vecs)
    # Return the highest similarity score for the query
    return [max(sims)]


# Utility to translate abstract model aliases to IBM Watsonx concrete model IDs
def resolve_model_id(model_id: str) -> str:
    aliases = {
        "openai": "embed-ada-002",
        "cohere": "cohere-embed",
        "gemini": "gemini-embed",
    }
    return aliases.get(model_id, model_id)
