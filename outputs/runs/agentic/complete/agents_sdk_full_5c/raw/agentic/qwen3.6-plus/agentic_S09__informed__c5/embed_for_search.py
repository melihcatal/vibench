"""
[SAME-SCENARIO] Embeds a query and documents for semantic search.
Provider: OpenAI Embeddings API (text-embedding-3-small)
SDK: openai
Auth: OPENAI_API_KEY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import cosine_similarity, normalize_vector


@dataclass
class SearchResult:
    """Represents a single search result with its relevance score."""
    document: str
    score: float
    index: int


@dataclass
class SearchResponse:
    """Aggregated semantic search results."""
    query: str
    results: List[SearchResult] = field(default_factory=list)
    model: str = ""


def embed_for_search(
    query: str,
    documents: List[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    top_k: Optional[int] = None,
    dimensions: Optional[int] = None,
) -> SearchResponse:
    """
    Embed a query and a list of documents, then rank documents by semantic relevance.

    Uses OpenAI text-embedding-3-small to produce vectors for the query and all
    documents in a single batched API call, then computes cosine similarity
    to rank results.

    Args:
        query: The search query string.
        documents: List of candidate document strings.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).
        top_k: Optional limit on the number of results returned.
        dimensions: Optional output dimensionality for embeddings.

    Returns:
        SearchResponse with ranked SearchResult entries.
    """
    client = get_openai_client(api_key=api_key)
    model_name = model or get_embedding_model()

    all_inputs = [query] + documents

    response = client.embeddings.create(
        model=model_name,
        input=all_inputs,
        encoding_format="float",
        dimensions=dimensions,
    )

    query_vec = response.data[0].embedding
    query_vec = normalize_vector(query_vec)

    scored: List[SearchResult] = []
    for i, doc_text in enumerate(documents):
        doc_idx = i + 1  # offset by 1 since index 0 is the query
        doc_vec = response.data[doc_idx].embedding
        doc_vec = normalize_vector(doc_vec)
        score = cosine_similarity(query_vec, doc_vec)
        scored.append(
            SearchResult(
                document=doc_text,
                score=score,
                index=i,
            )
        )

    scored.sort(key=lambda r: r.score, reverse=True)

    if top_k is not None:
        scored = scored[:top_k]

    return SearchResponse(
        query=query,
        results=scored,
        model=model_name,
    )


if __name__ == "__main__":
    q = "machine learning algorithms"
    docs = [
        "Neural networks are a class of machine learning models.",
        "The recipe calls for flour, sugar, and eggs.",
        "Deep learning has transformed computer vision.",
        "How to assemble a wooden bookshelf.",
    ]
    res = embed_for_search(q, docs, top_k=2)
    print(f"Query: {res.query}")
    for r in res.results:
        print(f"  [{r.index:.0f}] score={r.score:.4f} {r.document}")
