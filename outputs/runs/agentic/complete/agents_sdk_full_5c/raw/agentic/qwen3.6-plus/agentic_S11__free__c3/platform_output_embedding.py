"""Embed platform outputs for evaluation or retrieval using OpenAI embeddings.

Uses the OpenAI Embeddings API with the text-embedding-3-small model
to generate vector representations of platform model outputs for
semantic evaluation, similarity search, or retrieval-augmented generation.
"""

from typing import Dict, Any, Optional, List

from model_client import load_platform_config, get_openai_client
from model_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


def embed_platform_output(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> EmbeddingResult:
    """Embed platform model output using the OpenAI Embeddings API.

    Generates a vector embedding for the provided text using the
    text-embedding-3-small model for use in evaluation or retrieval.

    Args:
        text: The text output to embed.
        model: Override the default embedding model identifier.
        dimensions: Optional dimensionality for the embedding vector.
        provider_config: Optional pre-loaded OpenAI configuration.

    Returns:
        EmbeddingResult with the vector embedding and metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("embedding_model", OPENAI_EMBEDDING_MODEL)
    client = get_openai_client(provider_config)

    create_kwargs: Dict[str, Any] = {
        "model": model_id,
        "input": text,
    }

    if dimensions is not None:
        create_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**create_kwargs)

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding
    actual_dimensions = len(embedding_vector)

    return EmbeddingResult(
        text=text,
        embedding=embedding_vector,
        model=model_id,
        dimensions=actual_dimensions,
        provider="openai",
    )


def embed_batch_outputs(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> List[EmbeddingResult]:
    """Embed multiple platform outputs in a batch request.

    Args:
        texts: List of texts to embed.
        model: Embedding model override.
        dimensions: Optional dimensionality override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of EmbeddingResult objects, one per input text.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("embedding_model", OPENAI_EMBEDDING_MODEL)
    client = get_openai_client(provider_config)

    create_kwargs: Dict[str, Any] = {
        "model": model_id,
        "input": texts,
    }

    if dimensions is not None:
        create_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**create_kwargs)

    results = []
    for i, data in enumerate(response.data):
        results.append(
            EmbeddingResult(
                text=texts[i],
                embedding=data.embedding,
                model=model_id,
                dimensions=len(data.embedding),
                provider="openai",
            )
        )

    return results


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding dimensions must match")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def embed_and_compare(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Embed two texts and compute their similarity score.

    Args:
        text_a: First text to compare.
        text_b: Second text to compare.
        model: Embedding model override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with embeddings and similarity score.
    """
    result_a = embed_platform_output(text_a, model=model, provider_config=provider_config)
    result_b = embed_platform_output(text_b, model=model, provider_config=provider_config)

    similarity = compute_similarity(result_a.embedding, result_b.embedding)

    return {
        "text_a": text_a,
        "text_b": text_b,
        "embedding_a": result_a.embedding,
        "embedding_b": result_b.embedding,
        "similarity": similarity,
        "model": result_a.model,
        "provider": "openai",
    }


def get_embedding_model_info(
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Get information about the configured embedding model.

    Args:
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with embedding model metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = provider_config.get("embedding_model", OPENAI_EMBEDDING_MODEL)

    return {
        "model": model_id,
        "default_dimensions": OPENAI_EMBEDDING_DIMENSIONS,
        "provider": "openai",
        "max_input_tokens": 8191,
    }
