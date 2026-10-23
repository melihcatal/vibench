"""
embed_for_search.py - Embeds a query and documents for semantic search.

Provider: OpenAI Embeddings API
Model: text-embedding-3-small
SDK: openai
Auth: OPENAI_API_KEY
"""

from dataclasses import dataclass
from typing import Optional

from embeddings_client import get_openai_client, resolve_model
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingVector,
    parse_openai_embedding_response,
    cosine_similarity,
)


@dataclass
class SearchResult:
    """A single search result with its relevance score."""

    document: str
    score: float
    rank: int


def embed_for_search(
    query: str,
    documents: list[str],
    model: str | None = None,
    top_k: int | None = None,
) -> list[SearchResult]:
    """Embed a query and a list of documents, then rank by cosine similarity.

    Uses the OpenAI Embeddings API (text-embedding-3-small) to produce
    vectors for the query and all documents in a single batch call when possible.

    Args:
        query: The search query string.
        documents: List of document strings to search over.
        model: OpenAI embedding model (default: text-embedding-3-small).
        top_k: Optional limit on number of results returned.

    Returns:
        List of SearchResult ranked by descending similarity score.
    """
    client = get_openai_client()
    resolved_model = resolve_model(model)

    all_inputs = [query] + documents
    request = EmbeddingRequest(
        input=all_inputs,
        model=resolved_model,
    )

    response = client.embeddings.create(**request.to_openai_params())
    parsed = parse_openai_embedding_response(response)

    if len(parsed.vectors) < len(all_inputs):
        raise RuntimeError("Did not receive enough vectors from OpenAI Embeddings API")

    query_vector = parsed.vectors[0].vector
    results: list[SearchResult] = []

    for i, doc in enumerate(documents):
        doc_vector = parsed.vectors[i + 1].vector
        score = cosine_similarity(query_vector, doc_vector)
        results.append(SearchResult(document=doc, score=score, rank=0))

    results.sort(key=lambda r: r.score, reverse=True)

    for rank, result in enumerate(results, start=1):
        result.rank = rank

    if top_k is not None:
        results = results[:top_k]

    return results


def main() -> None:
    query = "machine learning frameworks for deep neural networks"
    documents = [
        "PyTorch is a widely used deep learning framework developed by Meta.",
        "React is a JavaScript library for building user interfaces.",
        "TensorFlow provides comprehensive tools for training ML models at scale.",
        "SQL databases store structured relational data efficiently.",
        "JAX composes numerical computing with automatic differentiation.",
    ]

    results = embed_for_search(query, documents, top_k=3)
    print(f"Query: {query}\n")
    for r in results:
        print(f"  [{r.rank}] score={r.score:.4f} -> {r.document}")


if __name__ == "__main__":
    main()
