"""
Same-scenario: Embed a query and documents for semantic search.
Provider: OpenAI Embeddings API via openai SDK.
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

from typing import Dict, List, Optional, Tuple

from embeddings_client import create_embeddings_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import EmbeddingResponse, cosine_similarity, parse_openai_embedding_response


def embed_for_search(
    query: str,
    documents: List[str],
    top_k: int = 5,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[Tuple[int, float, str]]:
    """Embed a query and a list of documents, then return ranked results.

    Uses OpenAI text-embedding-3-small to generate embeddings for the query
    and all documents in batch, then ranks by cosine similarity.

    Args:
        query: The search query string.
        documents: List of document texts to search over.
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: Optional override for OPENAI_API_KEY.

    Returns:
        List of (document_index, similarity_score, document_text) tuples,
        sorted by descending similarity.
    """
    resolved_model = model or DEFAULT_EMBEDDING_MODEL
    client = create_embeddings_client(api_key=api_key)

    # Embed query + all documents in a single batch when possible
    all_texts = [query] + documents
    request_kwargs = {
        "input": all_texts,
        "model": resolved_model,
        "encoding_format": "float",
    }
    if dimensions is not None:
        request_kwargs["dimensions"] = dimensions

    raw_response = client.embeddings.create(**request_kwargs)

    query_resp = parse_openai_embedding_response(raw_response, index=0)
    query_vec = query_resp.embedding

    doc_results: List[Tuple[int, float, str]] = []
    for i, doc_text in enumerate(documents):
        doc_resp = parse_openai_embedding_response(raw_response, index=i + 1)
        score = cosine_similarity(query_vec, doc_resp.embedding)
        doc_results.append((i, score, doc_text))

    doc_results.sort(key=lambda x: x[1], reverse=True)
    return doc_results[:top_k]


if __name__ == "__main__":
    docs = [
        "OpenAI provides powerful language models and embedding APIs.",
        "The capital of France is Paris.",
        "Embeddings convert text into numerical vector representations.",
        "Python is widely used for data science and machine learning.",
        "Semantic search uses vector similarity to find relevant documents.",
    ]
    results = embed_for_search("How does semantic search work?", docs, top_k=3)
    for idx, score, text in results:
        print(f"[{idx}] score={score:.4f} | {text}")
