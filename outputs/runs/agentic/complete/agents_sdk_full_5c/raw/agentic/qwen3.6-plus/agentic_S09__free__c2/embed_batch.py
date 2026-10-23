"""
[SAME-SCENARIO] Generates embeddings for a batch of texts.
Provider: OpenAI embeddings API (api.openai.com, model text-embedding-3-small).
"""

from embeddings_client import configure_client
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingResult,
    chunk_texts,
)


def embed_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
    dimensions: int | None = None,
) -> list[EmbeddingResult]:
    """
    Generate embedding vectors for a batch of text strings using the
    OpenAI embeddings API (api.openai.com).

    Automatically chunks the input into sub-batches to respect the
    provider's per-request limit.

    Args:
        texts: List of text strings to embed.
        model: OpenAI model identifier (default: text-embedding-3-small).
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var).
        dimensions: Optional output dimensionality.

    Returns:
        A list of EmbeddingResult objects with vectors and metadata.
    """
    client, _ = configure_client(api_key=api_key)

    all_results: list[EmbeddingResult] = []
    total_tokens = 0

    for chunk in chunk_texts(texts):
        request = EmbeddingRequest(
            input_texts=chunk,
            model=model,
            dimensions=dimensions,
        )

        raw_response = client.embeddings.create(**request.to_openai_kwargs())
        chunk_response = EmbeddingResponse.from_openai_response(raw_response, chunk)

        total_tokens += chunk_response.total_tokens
        all_results.extend(chunk_response.results)

    return all_results


if __name__ == "__main__":
    batch_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a versatile programming language.",
        "Machine learning models require large datasets.",
    ]
    results = embed_batch(batch_texts)
    for r in results:
        print(f"[{r.index}] len={len(r.vector)} text={r.text[:40]}...")
