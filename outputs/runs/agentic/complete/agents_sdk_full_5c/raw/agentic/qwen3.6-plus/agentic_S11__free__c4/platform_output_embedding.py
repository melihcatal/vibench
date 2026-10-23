"""Embed platform outputs for evaluation or retrieval.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
Uses concrete Azure OpenAI embedding model families such as
text-embedding-ada-002, text-embedding-3-small, and text-embedding-3-large.
"""

from __future__ import annotations

import os
from typing import Optional

import numpy as np
from openai import AzureOpenAI

from model_client import build_azure_openai_client


# Default Azure OpenAI embedding deployment name and model identifier
_AZURE_EMBEDDING_DEPLOYMENT_ENV = "AZURE_EMBEDDING_DEPLOYMENT"
_DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
_DEFAULT_EMBEDDING_DEPLOYMENT = os.environ.get(
    _AZURE_EMBEDDING_DEPLOYMENT_ENV, "text-embedding-ada-002"
)

# Azure OpenAI embedding model family identifiers
AZURE_EMBEDDING_MODELS = [
    "text-embedding-ada-002",
    "text-embedding-3-small",
    "text-embedding-3-large",
]


def get_default_embedding_deployment() -> str:
    """Return the default Azure OpenAI embedding deployment name."""
    return _DEFAULT_EMBEDDING_DEPLOYMENT


def platform_output_embedding(
    *,
    text: str,
    deployment_id: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
    dimensions: Optional[int] = None,
) -> list[float]:
    """Generate an embedding vector for platform model output text.

    Sends the text to an Azure OpenAI embedding deployment and returns
    the raw embedding vector as a list of floats.

    Azure OpenAI supports embedding models like text-embedding-ada-002,
    text-embedding-3-small, and text-embedding-3-large. The text-embedding-3
    family supports the optional dimensions parameter to reduce output size.

    Args:
        text: The text to embed (typically model output).
        deployment_id: Azure OpenAI embedding deployment name. Defaults to env or 'text-embedding-ada-002'.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        dimensions: Optional output dimension count (only supported by text-embedding-3-* models).

    Returns:
        Embedding vector as a list of floats.
    """
    if client is None:
        client = build_azure_openai_client()

    resolved_deployment = deployment_id or get_default_embedding_deployment()

    create_kwargs: dict = {
        "model": resolved_deployment,
        "input": text,
    }

    if dimensions is not None:
        create_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**create_kwargs)

    if response.data:
        return response.data[0].embedding

    raise RuntimeError(
        f"Azure OpenAI embedding deployment '{resolved_deployment}' returned no data."
    )


def batch_embed_platform_outputs(
    *,
    texts: list[str],
    deployment_id: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
    dimensions: Optional[int] = None,
) -> list[list[float]]:
    """Generate embeddings for multiple platform output texts in a single request.

    Azure OpenAI's embedding API accepts an array of input strings, up to
    the model's maximum batch size.

    Args:
        texts: List of texts to embed.
        deployment_id: Azure OpenAI embedding deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        dimensions: Optional output dimension count.

    Returns:
        List of embedding vectors, one per input text in order.
    """
    if client is None:
        client = build_azure_openai_client()

    resolved_deployment = deployment_id or get_default_embedding_deployment()

    create_kwargs: dict = {
        "model": resolved_deployment,
        "input": texts,
    }

    if dimensions is not None:
        create_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**create_kwargs)

    # Sort by index to ensure order matches input
    embeddings_by_index = {
        item.index: item.embedding for item in response.data
    }

    return [embeddings_by_index[i] for i in range(len(texts))]


def compute_cosine_similarity(
    embedding_a: list[float],
    embedding_b: list[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between -1.0 and 1.0.
    """
    vec_a = np.array(embedding_a)
    vec_b = np.array(embedding_b)

    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))


def embed_and_evaluate_similarity(
    *,
    text_a: str,
    text_b: str,
    deployment_id: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
    dimensions: Optional[int] = None,
) -> float:
    """Embed two platform outputs and compute their cosine similarity.

    Useful for evaluating model output quality, semantic similarity of
    paraphrases, or retrieval-augmented generation scoring.

    Args:
        text_a: First text to compare.
        text_b: Second text to compare.
        deployment_id: Azure OpenAI embedding deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        dimensions: Optional output dimension count.

    Returns:
        Cosine similarity score.
    """
    emb_a = platform_output_embedding(
        text=text_a,
        deployment_id=deployment_id,
        client=client,
        dimensions=dimensions,
    )
    emb_b = platform_output_embedding(
        text=text_b,
        deployment_id=deployment_id,
        client=client,
        dimensions=dimensions,
    )

    return compute_cosine_similarity(emb_a, emb_b)


def build_retrieval_index(
    *,
    texts: list[str],
    deployment_id: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
    dimensions: Optional[int] = None,
) -> list[dict]:
    """Build a simple retrieval index from platform output embeddings.

    Each entry contains the original text, its index, and the embedding vector
    for similarity search.

    Args:
        texts: List of texts to index.
        deployment_id: Azure OpenAI embedding deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        dimensions: Optional output dimension count.

    Returns:
        List of index entries with text, index, and embedding.
    """
    embeddings = batch_embed_platform_outputs(
        texts=texts,
        deployment_id=deployment_id,
        client=client,
        dimensions=dimensions,
    )

    return [
        {
            "index": i,
            "text": texts[i],
            "embedding": embeddings[i],
        }
        for i in range(len(texts))
    ]


def search_retrieval_index(
    *,
    query_text: str,
    index: list[dict],
    deployment_id: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
    top_k: int = 3,
    dimensions: Optional[int] = None,
) -> list[dict]:
    """Search a retrieval index for the most similar entries to a query.

    Args:
        query_text: The query text to search for.
        index: The retrieval index built by build_retrieval_index.
        deployment_id: Azure OpenAI embedding deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        top_k: Number of top results to return.
        dimensions: Optional output dimension count.

    Returns:
        List of matching index entries sorted by similarity, limited to top_k.
    """
    query_embedding = platform_output_embedding(
        text=query_text,
        deployment_id=deployment_id,
        client=client,
        dimensions=dimensions,
    )

    scored = []
    for entry in index:
        similarity = compute_cosine_similarity(query_embedding, entry["embedding"])
        scored.append((similarity, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [entry for _, entry in scored[:top_k]]
