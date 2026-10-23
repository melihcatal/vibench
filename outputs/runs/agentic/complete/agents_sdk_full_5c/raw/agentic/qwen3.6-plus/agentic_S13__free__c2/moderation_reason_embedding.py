"""
moderation_reason_embedding.py - Embed moderation rationales for case retrieval.

Uses the OpenAI Embeddings API (api.openai.com) with the text-embedding-3-small model
to create vector embeddings of moderation rationales for similarity search and case retrieval.
"""

import os
import openai


EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536


def _get_openai_client():
    """Create an OpenAI client for embeddings API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def embed_moderation_reason(
    reason_text: str,
    model: str = EMBEDDING_MODEL,
    dimensions: int = None,
) -> dict:
    """
    Create an embedding for a moderation rationale text.

    Args:
        reason_text: The moderation rationale or reason text to embed.
        model: Embedding model to use (default: text-embedding-3-small).
        dimensions: Optional output dimensionality (for text-embedding-3 models).

    Returns:
        Dictionary with:
            - embedding: list of floats (the vector)
            - model: embedding model used
            - dimensions: actual dimension count
            - provider: openai
    """
    client = _get_openai_client()

    params = {
        "input": reason_text,
        "model": model,
    }
    if dimensions and model.startswith("text-embedding-3"):
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    embedding = response.data[0].embedding
    actual_dimensions = len(embedding)

    return {
        "embedding": embedding,
        "model": model,
        "dimensions": actual_dimensions,
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/embeddings",
    }


def embed_moderation_rationale_with_metadata(
    rationale: str,
    case_id: str,
    categories: list = None,
    model: str = EMBEDDING_MODEL,
) -> dict:
    """
    Embed a moderation rationale with associated metadata.

    Args:
        rationale: The moderation reason text.
        case_id: Unique identifier for the moderation case.
        categories: List of moderation categories that were triggered.
        model: Embedding model to use.

    Returns:
        Dict with embedding and metadata for case storage.
    """
    # Format rationale with context for richer embeddings
    context_text = f"Case {case_id}: {rationale}"
    if categories:
        context_text += f" Categories: {', '.join(categories)}"

    result = embed_moderation_reason(context_text, model=model)

    return {
        "case_id": case_id,
        "embedding": result["embedding"],
        "dimensions": result["dimensions"],
        "model": model,
        "categories": categories or [],
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/embeddings",
    }


def embed_batch_rationales(
    rationales: list[dict],
    model: str = EMBEDDING_MODEL,
    dimensions: int = None,
) -> list[dict]:
    """
    Embed a batch of moderation rationales in a single API call.

    Args:
        rationales: List of dicts with 'text' and 'case_id' keys.
        model: Embedding model to use.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding results with case IDs.
    """
    client = _get_openai_client()

    texts = [r["text"] for r in rationales]

    params = {
        "input": texts,
        "model": model,
    }
    if dimensions and model.startswith("text-embedding-3"):
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    results = []
    for idx, data in enumerate(response.data):
        results.append({
            "case_id": rationales[idx].get("case_id", f"case_{idx}"),
            "embedding": data.embedding,
            "dimensions": len(data.embedding),
            "model": model,
            "provider": "openai",
        })

    return results


def compute_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    import math

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = math.sqrt(sum(a * a for a in embedding_a))
    norm_b = math.sqrt(sum(b * b for b in embedding_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def find_similar_cases(
    query_rationale: str,
    case_embeddings: list[dict],
    top_k: int = 5,
    model: str = EMBEDDING_MODEL,
) -> list[dict]:
    """
    Find the most similar moderation cases to a query rationale.

    Args:
        query_rationale: The rationale text to search with.
        case_embeddings: List of stored case embeddings with case metadata.
        top_k: Number of similar cases to return.
        model: Embedding model for the query.

    Returns:
        List of similar cases sorted by similarity score.
    """
    query_result = embed_moderation_reason(query_rationale, model=model)
    query_embedding = query_result["embedding"]

    similarities = []
    for case in case_embeddings:
        sim = compute_similarity(query_embedding, case["embedding"])
        similarities.append({
            "case_id": case.get("case_id"),
            "similarity_score": sim,
            "categories": case.get("categories", []),
            "metadata": case.get("metadata", {}),
        })

    similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
    return similarities[:top_k]


if __name__ == "__main__":
    sample_rationale = "Content contains harassment directed at a specific individual with threatening language."
    result = embed_moderation_reason(sample_rationale)
    print(f"Model: {result['model']}")
    print(f"Dimensions: {result['dimensions']}")
    print(f"Embedding preview: {result['embedding'][:5]}...")
