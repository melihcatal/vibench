"""
Embeds a query and documents for semantic search.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from embeddings_client import EmbeddingsClient
from embeddings_models import cosine_similarity, SearchResult


def embed_for_search(
    query: str,
    documents: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
    top_k: int = 5,
) -> list[SearchResult]:
    """Embed a query and documents, then rank by cosine similarity using OpenAI.

    Args:
        query: Search query string.
        documents: List of document strings to search over.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Output embedding dimensions.
        top_k: Number of top results to return.

    Returns:
        Sorted list of SearchResult ranked by similarity score descending.
    """
    client = EmbeddingsClient(model=model, dimensions=dimensions)

    # Embed the query
    query_embedding = client.embed(text=query, dimensions=dimensions)

    # Embed all documents in a single batch call to api.openai.com
    doc_embeddings = client.embed_many(texts=documents, dimensions=dimensions)

    # Score each document against the query
    scored_results: list[SearchResult] = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scored_results.append(SearchResult(document=documents[i], score=score, index=i))

    # Sort by score descending and return top_k
    scored_results.sort(key=lambda r: r.score, reverse=True)
    return scored_results[:top_k]


if __name__ == "__main__":
    query = "How do I train a neural network?"
    docs = [
        "Neural networks are trained using backpropagation and gradient descent.",
        "The capital of France is Paris.",
        "Deep learning requires large datasets and GPU acceleration.",
        "Convolutional neural networks excel at image recognition tasks.",
        "A recipe for chocolate chip cookies.",
    ]
    results = embed_for_search(query, docs, top_k=3)
    for r in results:
        print(f"[{r.score:.4f}] {r.document}")
