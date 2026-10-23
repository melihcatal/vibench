"""
Embeds a query and documents for semantic search using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: text-embedding-3-small
"""

import sys
from typing import List, Dict, Any, Optional, Tuple

from embeddings_client import get_openai_client, resolve_model
from embeddings_models import (
    EmbeddingRequest,
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    cosine_similarity,
    normalize_vector,
)


def embed_query_and_documents(
    query: str,
    documents: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Tuple[List[float], List[List[float]]]:
    """
    Embed a query and a list of documents for semantic search.

    Args:
        query: The search query string.
        documents: List of document strings to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Output dimensionality for embeddings.
        api_key: OpenAI API key.

    Returns:
        Tuple of (query_embedding, list_of_document_embeddings).
    """
    resolved_model = resolve_model(model)

    client = get_openai_client(api_key=api_key)

    all_texts = [query] + documents
    request = BatchEmbeddingRequest(
        texts=all_texts,
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    query_embedding = batch_result.embeddings[0]
    doc_embeddings = batch_result.embeddings[1:]

    return query_embedding, doc_embeddings


def semantic_search_rank(
    query: str,
    documents: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Perform semantic search by embedding query and documents, then ranking by similarity.

    Args:
        query: The search query string.
        documents: List of document strings to search.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        top_k: Number of top results to return.
        api_key: OpenAI API key.

    Returns:
        List of dicts with 'index', 'document', 'similarity_score', sorted by score descending.
    """
    query_embedding, doc_embeddings = embed_query_and_documents(
        query, documents, model=model, dimensions=dimensions, api_key=api_key
    )

    query_vec = normalize_vector(query_embedding)

    scored_results = []
    for i, doc_vec in enumerate(doc_embeddings):
        doc_vec_norm = normalize_vector(doc_vec)
        score = cosine_similarity(query_vec, doc_vec_norm)
        scored_results.append({
            "index": i,
            "document": documents[i],
            "similarity_score": score,
        })

    scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return scored_results[:top_k]


def semantic_search_with_metadata(
    query: str,
    documents: List[Dict[str, Any]],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on documents with metadata.

    Args:
        query: The search query string.
        documents: List of dicts, each containing 'text' key and optional metadata.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        top_k: Number of top results to return.
        api_key: OpenAI API key.

    Returns:
        List of dicts with original metadata plus similarity_score, sorted by score.
    """
    texts = [doc.get("text", "") for doc in documents]

    query_embedding, doc_embeddings = embed_query_and_documents(
        query, texts, model=model, dimensions=dimensions, api_key=api_key
    )

    query_vec = normalize_vector(query_embedding)

    scored_results = []
    for i, doc_vec in enumerate(doc_embeddings):
        doc_vec_norm = normalize_vector(doc_vec)
        score = cosine_similarity(query_vec, doc_vec_norm)

        result = {**documents[i], "similarity_score": score, "original_index": i}
        scored_results.append(result)

    scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return scored_results[:top_k]


if __name__ == "__main__":
    query_text = sys.argv[1] if len(sys.argv) > 1 else "machine learning"
    doc_list = [
        "Python programming basics and syntax.",
        "Introduction to neural networks and deep learning.",
        "Data visualization techniques with matplotlib.",
        "Natural language processing fundamentals.",
    ]

    results = semantic_search_rank(query_text, doc_list, top_k=3)
    print(f"Query: {query_text}")
    for r in results:
        print(f"Score: {r['similarity_score']:.4f} | {r['document']}")
