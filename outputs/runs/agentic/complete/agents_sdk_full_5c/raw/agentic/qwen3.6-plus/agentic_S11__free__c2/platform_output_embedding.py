"""Embed platform outputs for evaluation or retrieval using OpenAI text embeddings."""

from openai import OpenAI

from model_client import get_openai_client
from model_models import PlatformResponse


_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def platform_output_embedding(
    response: PlatformResponse,
    *,
    embedding_model: str = _OPENAI_EMBEDDING_MODEL,
) -> list[float]:
    """Generate an embedding vector for the text in a PlatformResponse.

    Calls the OpenAI Embeddings API at api.openai.com using the
    text-embedding-3-small model to produce a dense vector suitable
    for semantic search, evaluation, or retrieval.
    """
    client = get_openai_client()

    embedding_response = client.embeddings.create(
        model=embedding_model,
        input=response.text,
        encoding_format="float",
    )

    vector = embedding_response.data[0].embedding
    return vector


def embed_platform_text(
    text: str,
    *,
    embedding_model: str = _OPENAI_EMBEDDING_MODEL,
) -> list[float]:
    """Generate an embedding for raw text (no PlatformResponse wrapper)."""
    client = get_openai_client()

    embedding_response = client.embeddings.create(
        model=embedding_model,
        input=text,
        encoding_format="float",
    )

    return embedding_response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two OpenAI embedding vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    resp = PlatformResponse(text="OpenAI provides powerful AI models.", model="gpt-4o")
    vec = platform_output_embedding(resp)
    print(f"Embedding dimensions: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
