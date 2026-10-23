"""
[SAME-SCENARIO] Embeds a query and documents for semantic search.
Provider: OpenAI embeddings API (api.openai.com, model text-embedding-3-small).
"""

from __future__ import annotations

from dataclasses import dataclass

from embeddings_client import configure_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, cosine_similarity


@dataclass
class SearchResult:
    """A single search result with its similarity score."""
    text: str
    score: float
    index: int


def embed_for_search(
    query: str,
    documents: list[str],
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
    top_k: int = 5,
) -> list[SearchResult]:
    """
    Embed a query and a list of documents, then rank documents by
    cosine similarity to the query using the OpenAI embeddings API
    (api.openai.com, model text-embedding-3-small).

    Args:
        query: The search query string.
        documents: List of document strings to search over.
        model: OpenAI model identifier.
        api_key: OpenAI API key.
        top_k: Number of top results to return.

    Returns:
        List of SearchResult objects ranked by descending similarity.
    """
    client, _ = configure_client(api_key=api_key)

    all_texts = [query] + documents
    request = EmbeddingRequest(input_texts=all_texts, model=model)

    raw_response = client.embeddings.create(**request.to_openai_kwargs())
    response = EmbeddingResponse.from_openai_response(raw_response, all_texts)

    query_vector = response.results[0].vector
    doc_results: list[SearchResult] = []

    for i, doc_embedding in enumerate(response.results[1:], start=0):
        score = cosine_similarity(query_vector, doc_embedding.vector)
        doc_results.append(
            SearchResult(
                text=documents[i],
                score=score,
                index=i,
            )
        )

    doc_results.sort(key=lambda r: r.score, reverse=True)
    return doc_results[:top_k]


if __name__ == "__main__":
    docs = [
        "The Eiffel Tower is located in Paris, France.",
        "Python programming language was created by Guido van Rossum.",
        "The Amazon rainforest is the largest tropical rainforest.",
        "OpenAI develops advanced artificial intelligence systems.",
        "Mount Everest is the highest mountain in the world.",
    ]

    results = embed_for_search("What is the tallest peak on Earth?", docs, top_k=3)
    for r in results:
        print(f"[{r.index}] score={r.score:.4f} text={r.text}")
