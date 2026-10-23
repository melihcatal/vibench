"""
Embed model outputs for clustering or retrieval using the OpenAI Embeddings API.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-small, text-embedding-3-large
"""

from __future__ import annotations

import os
from typing import List, Optional

from openai import OpenAI

from model_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_HOST = "api.openai.com"


def load_openai_api_key() -> str:
    """Load the OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Sign up at https://platform.openai.com/ to get your key."
        )
    return api_key


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create a configured OpenAI client for embeddings."""
    key = api_key or load_openai_api_key()
    return OpenAI(api_key=key)


def embed_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    """Embed a single text string using OpenAI's embeddings API.

    Args:
        text: The text to embed.
        model: Concrete OpenAI embedding model ID (e.g., 'text-embedding-3-small',
               'text-embedding-3-large').
        api_key: Optional override for the OpenAI API key.
        dimensions: Optional dimensionality truncation for supported models.

    Returns:
        EmbeddingResult with the embedding vector and metadata.
    """
    client = create_openai_client(api_key)

    kwargs: dict = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embedding_data = response.data[0].embedding
    usage_tokens = response.usage.prompt_tokens if response.usage else 0

    return EmbeddingResult(
        embeddings=[embedding_data],
        model=model,
        usage_prompt_tokens=usage_tokens,
        raw_response=response,
    )


def embed_texts(
    texts: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    """Embed multiple text strings using OpenAI's embeddings API.

    Args:
        texts: List of text strings to embed.
        model: Concrete OpenAI embedding model ID.
        api_key: Optional override for the OpenAI API key.
        dimensions: Optional dimensionality truncation.

    Returns:
        EmbeddingResult with all embedding vectors.
    """
    client = create_openai_client(api_key)

    kwargs: dict = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    all_embeddings = [item.embedding for item in response.data]
    usage_tokens = response.usage.prompt_tokens if response.usage else 0

    return EmbeddingResult(
        embeddings=all_embeddings,
        model=model,
        usage_prompt_tokens=usage_tokens,
        raw_response=response,
    )


def embed_model_output(
    generated_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> EmbeddingResult:
    """Convenience: embed a single model-generated output for retrieval or clustering."""
    return embed_text(text=generated_text, model=model)


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
