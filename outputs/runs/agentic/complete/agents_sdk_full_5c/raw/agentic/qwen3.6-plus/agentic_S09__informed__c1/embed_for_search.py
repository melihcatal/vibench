"""Embeds a query and documents for semantic search using OpenAI Embeddings API.

Uses the OpenAI text-embedding-3-small model to embed both the query and a
corpus of documents, then ranks documents by cosine similarity to the query.
"""

import os
from typing import List, Tuple

from embeddings_client import get_openai_client, create_batch_embeddings, get_embedding_model
from embeddings_models import rank_by_similarity, EmbeddingRequest


def embed_for_semantic_search(
    query: str,
    documents: List[str],
    model: str = None,
    dimensions: int = None,
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """Embed a query and documents, then rank by cosine similarity.

    Args:
        query: Search query text.
        documents: List of document texts to search over.
        model: OpenAI embedding model ID (defaults to OPENAI_EMBEDDING_MODEL env var).
        dimensions: Optional output dimensionality for embeddings.
        top_k: Number of top results to return.

    Returns:
        List of (document, similarity_score) tuples ranked by similarity.
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    all_texts = [query] + documents
    response = client.embeddings.create(
        input=all_texts,
        model=model_id,
        dimensions=dimensions if dimensions else None,
    )

    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]

    ranked = rank_by_similarity(query_embedding, document_embeddings, documents, top_k)
    return ranked


def embed_query_and_documents(
    query: str,
    documents: List[str],
    model: str = None,
    dimensions: int = None,
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and all documents separately.

    Args:
        query: Search query text.
        documents: List of document texts.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.

    Returns:
        Tuple of (query_embedding, list_of_document_embeddings).
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    query_response = client.embeddings.create(
        input=query,
        model=model_id,
        dimensions=dimensions if dimensions else None,
    )
    query_embedding = query_response.data[0].embedding

    doc_response = client.embeddings.create(
        input=documents,
        model=model_id,
        dimensions=dimensions if dimensions else None,
    )
    document_embeddings = [item.embedding for item in doc_response.data]

    return query_embedding, document_embeddings


def main():
    query = os.environ.get("SEARCH_QUERY", "machine learning techniques")
    documents = [
        "Neural networks are the backbone of deep learning systems.",
        "Linear regression is a basic statistical method for prediction.",
        "Decision trees split data based on feature thresholds.",
        "Transfer learning reuses pre-trained models for new tasks.",
        "Random forests combine multiple decision trees for robust predictions.",
    ]
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    top_k = int(os.environ.get("SEARCH_TOP_K", "3"))

    results = embed_for_semantic_search(query, documents, model=model, top_k=top_k)
    print(f"Query: {query}")
    print(f"Model: {model}")
    print(f"Top {top_k} results:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"  {i}. (score={score:.4f}) {doc}")


if __name__ == "__main__":
    main()
