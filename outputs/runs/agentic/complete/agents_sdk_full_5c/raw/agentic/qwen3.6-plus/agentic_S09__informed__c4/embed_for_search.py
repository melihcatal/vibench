"""
Embed a query and a list of documents for semantic search using OpenAI Embeddings API.

Uses the openai SDK with model text-embedding-3-small to embed both the
search query and the document corpus, returning embeddings suitable for
ranking by cosine similarity.
Requires OPENAI_API_KEY environment variable or explicit api_key parameter.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from openai import OpenAI

from embed_batch import embed_batch
from embed_text import embed_text
from embeddings_models import EmbeddingResponse, cosine_similarity, normalize_vector

OPENAI_MODEL = "text-embedding-3-small"
OPENAI_DEFAULT_DIMENSIONS = 1536


@dataclass
class SearchResult:
    """
    Represents a single search result with its document and similarity score.

    Attributes:
        document: The original document text.
        index: Index of the document in the input corpus.
        score: Cosine similarity between query and document embedding.
    """

    document: str
    index: int
    score: float


def embed_for_search(
    query: str,
    documents: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    normalize: bool = True,
    client: Optional[OpenAI] = None,
) -> Tuple[List[float], List[EmbeddingResponse]]:
    """
    Embed a query and a corpus of documents for semantic search.

    Uses OpenAI embeddings to produce a query vector and document vectors.
    All vectors use the same model for comparability.

    Args:
        query: The search query text.
        documents: List of candidate document texts.
        api_key: OpenAI API key.
        model: OpenAI embedding model identifier.
        dimensions: Output vector dimensions.
        normalize: Whether to L2-normalize all output vectors.
        client: Pre-configured OpenAI client (optional).

    Returns:
        Tuple of (query_embedding_vector, list_of_document_embedding_responses).
    """
    if not documents:
        return [], []

    query_response = embed_text(
        text=query,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        client=client,
    )
    query_vec = query_response.embedding

    doc_responses = embed_batch(
        texts=documents,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        client=client,
    )

    if normalize:
        query_vec = normalize_vector(query_vec)
        for resp in doc_responses:
            resp.embedding = normalize_vector(resp.embedding)

    return query_vec, doc_responses


def search_and_rank(
    query: str,
    documents: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    top_k: Optional[int] = None,
    normalize: bool = True,
    client: Optional[OpenAI] = None,
) -> List[SearchResult]:
    """
    Perform semantic search by embedding query and documents, then ranking.

    Args:
        query: Search query text.
        documents: Candidate document corpus.
        api_key: OpenAI API key.
        model: OpenAI embedding model ID.
        dimensions: Output dimensions.
        top_k: Return only the top K results (optional).
        normalize: L2-normalize vectors before scoring.
        client: Optional pre-built OpenAI client.

    Returns:
        List of SearchResult sorted by descending similarity score.
    """
    query_vec, doc_responses = embed_for_search(
        query=query,
        documents=documents,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        normalize=normalize,
        client=client,
    )

    if not query_vec or not doc_responses:
        return []

    results = []
    for idx, doc_resp in enumerate(doc_responses):
        score = cosine_similarity(query_vec, doc_resp.embedding)
        results.append(
            SearchResult(
                document=documents[idx],
                index=idx,
                score=score,
            )
        )

    results.sort(key=lambda r: r.score, reverse=True)

    if top_k is not None:
        results = results[:top_k]

    return results
