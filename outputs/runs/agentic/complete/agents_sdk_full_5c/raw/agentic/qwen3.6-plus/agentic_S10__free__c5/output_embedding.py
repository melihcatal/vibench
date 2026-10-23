"""
output_embedding.py - Embed model outputs for clustering or retrieval.

Uses OpenAI's Embeddings API (text-embedding-3-large model) hosted at api.openai.com.
"""

import math
from typing import Optional

from model_client import get_openai_client
from model_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL_LARGE = "text-embedding-3-large"
OPENAI_EMBEDDING_MODEL_SMALL = "text-embedding-3-small"
OPENAI_EMBEDDING_MODEL_ADA = "text-embedding-ada-002"

OPENAI_EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"


def embed_output(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL_LARGE,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    """
    Generate an embedding vector for a model output using OpenAI's Embeddings API.

    Args:
        text: The text output to embed.
        model: OpenAI embedding model ID (e.g. "text-embedding-3-large").
        dimensions: Optional dimensionality reduction for supported models.

    Returns:
        EmbeddingResult with the embedding vector and metadata.
    """
    client = get_openai_client()

    params = {
        "input": text,
        "model": model,
    }
    if dimensions is not None and model in (OPENAI_EMBEDDING_MODEL_LARGE, OPENAI_EMBEDDING_MODEL_SMALL):
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    if not response.data:
        raise ValueError("OpenAI embedding response returned no data")

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding

    return EmbeddingResult(
        embedding=embedding_vector,
        model_used=model,
        dimensions=len(embedding_vector),
        input_tokens=response.usage.prompt_tokens if response.usage else 0,
    )


def embed_multiple(
    texts: list[str],
    model: str = OPENAI_EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
) -> list[EmbeddingResult]:
    """
    Generate embeddings for multiple texts in a single batch API call.

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional dimensionality for supported models.

    Returns:
        List of EmbeddingResult objects.
    """
    client = get_openai_client()

    params = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None and model in (OPENAI_EMBEDDING_MODEL_LARGE, OPENAI_EMBEDDING_MODEL_SMALL):
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    results = []
    total_tokens = response.usage.prompt_tokens if response.usage else 0

    for item in response.data:
        results.append(EmbeddingResult(
            embedding=item.embedding,
            model_used=model,
            dimensions=len(item.embedding),
            input_tokens=total_tokens // len(texts) if texts else 0,
        ))

    return results


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def find_most_similar(
    query_text: str,
    candidate_texts: list[str],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL_SMALL,
) -> list[tuple[int, float, str]]:
    """
    Find the most similar texts to a query using OpenAI embeddings.

    Args:
        query_text: The query text to search with.
        candidate_texts: List of candidate texts to compare against.
        top_k: Number of top results to return.
        model: OpenAI embedding model.

    Returns:
        List of (index, similarity_score, text) tuples sorted by similarity.
    """
    query_result = embed_output(query_text, model=model)
    query_vec = query_result.embedding

    candidates_result = embed_multiple(candidate_texts, model=model)

    scored = []
    for idx, candidate in enumerate(candidates_result):
        sim = cosine_similarity(query_vec, candidate.embedding)
        scored.append((idx, sim, candidate_texts[idx]))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    sample_outputs = [
        "Machine learning is a subset of artificial intelligence.",
        "The weather today is sunny and warm.",
        "Deep learning uses neural networks with many layers.",
        "AI research has made significant progress in recent years.",
        "The stock market closed higher today.",
    ]

    print(f"Embedding model: {OPENAI_EMBEDDING_MODEL_SMALL}")
    results = embed_multiple(sample_outputs, model=OPENAI_EMBEDDING_MODEL_SMALL)
    for i, r in enumerate(results):
        print(f"  [{i}] dims={r.dimensions}, tokens={r.input_tokens}")
