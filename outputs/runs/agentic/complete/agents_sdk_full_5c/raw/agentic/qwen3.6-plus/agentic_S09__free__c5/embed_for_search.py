"""
Embed a query and documents for semantic search.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

from typing import List, Optional

from embeddings_client import (
    get_openai_client,
    load_embeddings_config,
    build_embeddings_payload,
    parse_embeddings_response,
)
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    SearchResult,
    format_search_results,
)


def embed_for_search(
    query: str,
    documents: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[SearchResult]:
    """
    Embed a query and a set of documents, then rank documents by semantic similarity.

    Uses OpenAI's text-embedding-3-small model to generate embeddings for both
    the query and all documents, then computes cosine similarity to rank results.

    Args:
        query: The search query text
        documents: List of document texts to search over
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        top_k: Number of top results to return
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)

    Returns:
        List of SearchResult objects ranked by similarity score (descending)

    Raises:
        ValueError: If query or documents are empty
        openai.APIError: If the OpenAI API request fails
    """
    if not query or not query.strip():
        raise ValueError("query cannot be empty")
    if not documents:
        raise ValueError("documents list cannot be empty")

    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    client = get_openai_client(api_key=api_key)

    all_texts = [query] + documents
    payload = build_embeddings_payload(
        texts=all_texts,
        model=target_model,
        dimensions=target_dimensions,
    )

    response = client.embeddings.create(**payload)
    all_embeddings = parse_embeddings_response(response)

    if len(all_embeddings) != len(all_texts):
        raise ValueError("Embedding count mismatch with input texts")

    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]

    results = format_search_results(
        query=query,
        documents=documents,
        query_embedding=query_embedding,
        document_embeddings=document_embeddings,
        top_k=top_k,
    )

    return results


def embed_query_and_documents(
    query: str,
    documents: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> tuple:
    """
    Embed query and documents separately, returning raw embeddings.

    Useful for caching embeddings or performing custom ranking.

    Args:
        query: The search query text
        documents: List of document texts
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        api_key: OpenAI API key

    Returns:
        Tuple of (query_embedding, document_embeddings_list)
    """
    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    client = get_openai_client(api_key=api_key)

    query_payload = build_embeddings_payload(
        texts=[query],
        model=target_model,
        dimensions=target_dimensions,
    )
    query_response = client.embeddings.create(**query_payload)
    query_embedding = parse_embeddings_response(query_response)[0]

    doc_embeddings = []
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        doc_payload = build_embeddings_payload(
            texts=batch,
            model=target_model,
            dimensions=target_dimensions,
        )
        doc_response = client.embeddings.create(**doc_payload)
        doc_embeddings.extend(parse_embeddings_response(doc_response))

    return query_embedding, doc_embeddings


if __name__ == "__main__":
    import json

    query = "How to train a neural network?"
    documents = [
        "Neural networks learn patterns from training data using backpropagation.",
        "Gradient descent optimizes model weights during training.",
        "Deep learning architectures include CNNs and RNNs.",
        "Transfer learning reuses pre-trained models for new tasks.",
    ]
    results = embed_for_search(query, documents, top_k=3)
    print(json.dumps({
        "query": query,
        "model": "text-embedding-3-small",
        "results": [
            {"rank": i + 1, "score": r.score, "document": r.document}
            for i, r in enumerate(results)
        ],
    }, indent=2))
