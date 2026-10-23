"""Embed a query and documents for semantic search using OpenAI embeddings API."""

import os
from typing import List, Dict, Optional, Tuple
import numpy as np
from openai import OpenAI

from embeddings_client import get_openai_client
from embeddings_models import normalize_vector
from similarity_score import cosine_similarity


def embed_for_search(
    query: str,
    documents: List[str],
    model: str = "text-embedding-3-small",
    top_k: int = 5,
) -> List[Dict]:
    """Embed a query and documents, then rank documents by semantic similarity.

    Uses OpenAI's text-embedding-3-small model for dense vector embeddings.
    This implements the core retrieval step for semantic search pipelines.

    Args:
        query: The search query text.
        documents: List of document texts to search over.
        model: OpenAI embedding model identifier.
        top_k: Number of top results to return.

    Returns:
        List of dicts with 'document', 'score', and 'index' keys, sorted by score.
    """
    client = get_openai_client()

    all_inputs = [query] + documents
    response = client.embeddings.create(
        input=all_inputs,
        model=model,
        encoding_format="float",
    )

    query_vector = np.array(response.data[0].embedding, dtype=np.float32)
    query_vector = normalize_vector(query_vector)

    results = []
    for i, doc_text in enumerate(documents):
        doc_vector = np.array(response.data[i + 1].embedding, dtype=np.float32)
        doc_vector = normalize_vector(doc_vector)
        score = cosine_similarity(query_vector, doc_vector)
        results.append({
            "document": doc_text,
            "score": float(score),
            "index": i,
            "embedding": doc_vector.tolist(),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def embed_query_only(
    query: str,
    model: str = "text-embedding-3-small",
) -> np.ndarray:
    """Embed just the query for reuse across multiple document sets."""
    client = get_openai_client()
    response = client.embeddings.create(
        input=query,
        model=model,
        encoding_format="float",
    )
    vec = np.array(response.data[0].embedding, dtype=np.float32)
    return normalize_vector(vec)


def embed_documents_only(
    documents: List[str],
    model: str = "text-embedding-3-small",
) -> List[np.ndarray]:
    """Embed just the documents for pre-computation and storage."""
    client = get_openai_client()

    all_vectors = []
    batch_size = 2048

    for i in range(0, len(documents), batch_size):
        chunk = documents[i : i + batch_size]
        response = client.embeddings.create(
            input=chunk,
            model=model,
            encoding_format="float",
        )
        for item in response.data:
            vec = np.array(item.embedding, dtype=np.float32)
            all_vectors.append(normalize_vector(vec))

    return all_vectors


def search_with_precomputed(
    query_vector: np.ndarray,
    document_vectors: List[np.ndarray],
    documents: List[str],
    top_k: int = 5,
) -> List[Dict]:
    """Rank pre-computed document vectors against a query vector."""
    results = []
    for i, doc_vec in enumerate(document_vectors):
        score = cosine_similarity(query_vector, doc_vec)
        results.append({
            "document": documents[i],
            "score": float(score),
            "index": i,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    query = "What are the benefits of renewable energy?"
    docs = [
        "Solar panels convert sunlight into electricity using photovoltaic cells.",
        "Wind turbines generate power by capturing kinetic energy from air currents.",
        "The company reported strong quarterly earnings last month.",
        "Renewable energy sources reduce greenhouse gas emissions significantly.",
        "Hydroelectric dams use flowing water to produce sustainable power.",
        "Electric vehicles are becoming more affordable and popular worldwide.",
    ]

    results = embed_for_search(query, docs, top_k=3)
    print(f"Query: {query}")
    for r in results:
        print(f"  Score: {r['score']:.4f} | {r['document'][:80]}...")
