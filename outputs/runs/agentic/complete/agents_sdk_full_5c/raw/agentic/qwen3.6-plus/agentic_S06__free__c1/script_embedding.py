"""
script_embedding.py - Embed narration scripts for voice-asset search using OpenAI Embeddings API.

Provider: OpenAI (https://api.openai.com)
Endpoint: POST https://api.openai.com/v1/embeddings
Model: text-embedding-3-small (default) or text-embedding-3-large
SDK: openai Python package
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"

# OpenAI embedding model identifiers
OPENAI_EMBEDDING_MODEL_SMALL = "text-embedding-3-small"
OPENAI_EMBEDDING_MODEL_LARGE = "text-embedding-3-large"
OPENAI_EMBEDDING_MODEL_ADA_002 = "text-embedding-ada-002"

# Default dimensions for OpenAI embedding models
EMBEDDING_DIMENSIONS = {
    OPENAI_EMBEDDING_MODEL_SMALL: 1536,
    OPENAI_EMBEDDING_MODEL_LARGE: 3072,
    OPENAI_EMBEDDING_MODEL_ADA_002: 1536,
}


@dataclass
class ScriptEmbedding:
    """Embedded narration script with metadata.

    Attributes:
        text: Original script text.
        embedding: Vector embedding from OpenAI.
        model: OpenAI embedding model used.
        metadata: Optional key-value metadata.
    """
    text: str
    embedding: List[float]
    model: str
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_numpy(self) -> np.ndarray:
        """Convert embedding to numpy array."""
        return np.array(self.embedding, dtype=np.float32)


def get_openai_client(
    api_key: Optional[str] = None,
) -> OpenAI:
    """Create an OpenAI API client for embeddings.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set "
            "or an explicit api_key must be provided."
        )
    return OpenAI(api_key=key)


def embed_script(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> ScriptEmbedding:
    """Embed a narration script using OpenAI Embeddings API.

    Generates a dense vector representation suitable for semantic
    search of voice assets.

    Args:
        text: Narration script text to embed.
        model: OpenAI embedding model (default: 'text-embedding-3-small').
        dimensions: Desired embedding dimensions (model-dependent).
        api_key: Optional explicit OpenAI API key override.
        metadata: Optional metadata to attach to the embedding.

    Returns:
        ScriptEmbedding with text, vector, and metadata.

    Raises:
        ValueError: If text is empty.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    client = get_openai_client(api_key=api_key)

    kwargs = {"model": model}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(
        input=text,
        **kwargs,
    )

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding

    return ScriptEmbedding(
        text=text,
        embedding=embedding_vector,
        model=model,
        metadata=metadata or {},
    )


def embed_scripts_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL_SMALL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    metadatas: Optional[List[Dict[str, str]]] = None,
) -> List[ScriptEmbedding]:
    """Embed multiple narration scripts in a single API call.

    OpenAI supports batch embedding with up to 2048 inputs per request.

    Args:
        texts: List of narration script texts to embed.
        model: OpenAI embedding model.
        dimensions: Desired embedding dimensions.
        api_key: Optional explicit OpenAI API key override.
        metadatas: Optional list of metadata dicts, one per text.

    Returns:
        List of ScriptEmbedding objects.
    """
    if not texts:
        return []

    client = get_openai_client(api_key=api_key)

    kwargs = {"model": model}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(
        input=texts,
        **kwargs,
    )

    embeddings = []
    for i, data in enumerate(response.data):
        meta = metadatas[i] if metadatas and i < len(metadatas) else {}
        embeddings.append(ScriptEmbedding(
            text=texts[i],
            embedding=data.embedding,
            model=model,
            metadata=meta,
        ))

    return embeddings


def compute_similarity(
    embedding_a: ScriptEmbedding,
    embedding_b: ScriptEmbedding,
) -> float:
    """Compute cosine similarity between two script embeddings.

    Args:
        embedding_a: First ScriptEmbedding.
        embedding_b: Second ScriptEmbedding.

    Returns:
        Cosine similarity score (0.0 to 1.0).
    """
    vec_a = embedding_a.to_numpy()
    vec_b = embedding_b.to_numpy()

    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def search_similar_scripts(
    query_embedding: ScriptEmbedding,
    candidates: List[ScriptEmbedding],
    top_k: int = 5,
    threshold: float = 0.0,
) -> List[Tuple[ScriptEmbedding, float]]:
    """Find the most similar scripts from a candidate pool.

    Args:
        query_embedding: Query ScriptEmbedding to match against.
        candidates: List of candidate ScriptEmbeddings to search.
        top_k: Maximum number of results to return.
        threshold: Minimum similarity score to include.

    Returns:
        List of (ScriptEmbedding, similarity_score) tuples, sorted by score.
    """
    scored = []
    for candidate in candidates:
        score = compute_similarity(query_embedding, candidate)
        if score >= threshold:
            scored.append((candidate, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def normalize_embedding(embedding: ScriptEmbedding) -> ScriptEmbedding:
    """L2-normalize an embedding vector for consistent similarity computation.

    Args:
        embedding: ScriptEmbedding to normalize.

    Returns:
        New ScriptEmbedding with normalized vector.
    """
    vec = embedding.to_numpy()
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return ScriptEmbedding(
        text=embedding.text,
        embedding=vec.tolist(),
        model=embedding.model,
        metadata=embedding.metadata,
    )


if __name__ == "__main__":
    sample_script = "Welcome to our guided tour of the museum's ancient artifacts collection."
    embedding = embed_script(sample_script)
    print(f"Embedded script using model: {embedding.model}")
    print(f"Embedding dimensions: {len(embedding.embedding)}")
    print(f"Text: {embedding.text[:60]}...")
