"""
[LATER-STEP] Embed platform outputs for evaluation or retrieval using Azure OpenAI.

Uses the Azure OpenAI text-embedding-3-large or text-embedding-3-small
deployment to generate vector embeddings from model-generated text content
for downstream similarity search, clustering, or evaluation tasks.
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_models import EmbeddingResult
from model_client import get_azure_openai_client, extract_token_usage


# Default Azure OpenAI embedding deployment names
AZURE_EMBEDDING_DEPLOYMENT_LARGE = "text-embedding-3-large"
AZURE_EMBEDDING_DEPLOYMENT_SMALL = "text-embedding-3-small"
AZURE_EMBEDDING_DEPLOYMENT_ADA = "text-embedding-ada-002"


def platform_output_embedding(
    text: str,
    deployment_name: str = AZURE_EMBEDDING_DEPLOYMENT_LARGE,
    dimensions: Optional[int] = None,
    client: Optional[AzureOpenAI] = None,
) -> EmbeddingResult:
    """
    Generate vector embeddings for platform output text using Azure OpenAI.

    Sends the text to the Azure OpenAI text embedding deployment and returns
    the resulting vector embedding along with metadata.

    Args:
        text: The text content to embed.
        deployment_name: Azure OpenAI embedding deployment name.
                         Defaults to 'text-embedding-3-large'.
        dimensions: Optional dimensionality reduction for the embedding.
                    Supported by text-embedding-3 models (e.g., 256, 512, 1024).
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        EmbeddingResult with the embedding vector and provider metadata.
    """
    if client is None:
        client = get_azure_openai_client()

    input_text = text.strip()
    if not input_text:
        raise ValueError("Input text for embedding cannot be empty")

    kwargs: dict = {
        "model": deployment_name,
        "input": input_text,
    }

    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    # Azure OpenAI embeddings response returns a list; take the first
    embedding_vector = response.data[0].embedding
    model_id = getattr(response, "model", deployment_name)
    usage = extract_token_usage(response)

    return EmbeddingResult(
        embedding=embedding_vector,
        model_id=model_id,
        deployment_name=deployment_name,
        usage=usage,
        raw_response=response,
    )


def batch_platform_output_embedding(
    texts: list[str],
    deployment_name: str = AZURE_EMBEDDING_DEPLOYMENT_LARGE,
    dimensions: Optional[int] = None,
    client: Optional[AzureOpenAI] = None,
) -> list[EmbeddingResult]:
    """
    Generate embeddings for multiple platform outputs via Azure OpenAI.

    Processes texts in batches respecting Azure OpenAI's input limits.
    Azure OpenAI embedding API supports up to 2048 input items per request
    for text-embedding-3 models.

    Args:
        texts: List of text strings to embed.
        deployment_name: Azure OpenAI embedding deployment name.
        dimensions: Optional dimensionality for the embeddings.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        List of EmbeddingResult objects, one per input text.
    """
    if client is None:
        client = get_azure_openai_client()

    if not texts:
        return []

    # Azure OpenAI batch embedding API supports multiple inputs
    cleaned_texts = [t.strip() for t in texts if t.strip()]
    if not cleaned_texts:
        return []

    # Process in chunks to stay within Azure OpenAI limits (max ~2048 items, ~8191 tokens)
    batch_size = 100  # Conservative batch size to stay within token limits
    results = []

    for i in range(0, len(cleaned_texts), batch_size):
        batch = cleaned_texts[i : i + batch_size]

        kwargs: dict = {
            "model": deployment_name,
            "input": batch,
        }

        if dimensions is not None:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        model_id = getattr(response, "model", deployment_name)
        usage = extract_token_usage(response)

        for idx, data_item in enumerate(response.data):
            results.append(
                EmbeddingResult(
                    embedding=data_item.embedding,
                    model_id=model_id,
                    deployment_name=deployment_name,
                    usage={
                        "batch_index": i // batch_size,
                        "item_index": idx,
                        "total_tokens": usage.get("total_tokens", 0),
                    },
                    raw_response=response,
                )
            )

    return results


def cosine_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Utility function for comparing embeddings generated by Azure OpenAI.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    import math

    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = math.sqrt(sum(a * a for a in embedding_a))
    norm_b = math.sqrt(sum(b * b for b in embedding_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)
