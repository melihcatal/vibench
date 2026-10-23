"""
embed_batch.py - Generates embeddings for a batch of texts.

Provider: OpenAI Embeddings API
Model: text-embedding-3-small
SDK: openai
Auth: OPENAI_API_KEY
"""

import sys

from embeddings_client import get_openai_client, resolve_model, chunk_texts
from embeddings_models import EmbeddingRequest, EmbeddingResponse, parse_openai_embedding_response


def embed_batch(
    texts: list[str],
    model: str | None = None,
    dimensions: int | None = None,
    max_batch_size: int = 50,
) -> EmbeddingResponse:
    """Generate embeddings for a batch of texts via the OpenAI Embeddings API.

    Handles OpenAI's batch limit by chunking the input list and aggregating results.

    Args:
        texts: List of input text strings to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Optional output dimensionality.
        max_batch_size: Maximum texts per API call (OpenAI limit is ~50).

    Returns:
        An EmbeddingResponse containing all vectors with original indices preserved.
    """
    client = get_openai_client()
    resolved_model = resolve_model(model)

    batches = chunk_texts(texts, max_batch_size)
    all_vectors: list = []
    total_tokens = 0
    final_model = resolved_model

    for batch_offset, batch in enumerate(batches):
        request = EmbeddingRequest(
            input=batch,
            model=resolved_model,
            dimensions=dimensions,
        )

        response = client.embeddings.create(**request.to_openai_params())
        parsed = parse_openai_embedding_response(response)

        for item in parsed.vectors:
            item.index += batch_offset * max_batch_size
            all_vectors.append(item)

        total_tokens += parsed.total_tokens
        if parsed.model:
            final_model = parsed.model

    return EmbeddingResponse(
        vectors=all_vectors,
        model=final_model,
        total_tokens=total_tokens,
    )


def main() -> None:
    sample_texts = [
        "OpenAI embeddings capture semantic meaning in dense vectors.",
        "Batch processing improves throughput for large document sets.",
        "Cosine similarity measures angular distance between vectors.",
        "The text-embedding-3-small model is efficient for production use.",
    ]

    result = embed_batch(sample_texts)
    print(f"Model: {result.model}")
    print(f"Total embeddings: {len(result.vectors)}")
    print(f"Total tokens used: {result.total_tokens}")
    for v in result.vectors:
        print(f"  [{v.index}] dim={len(v.vector)} first_3={v.vector[:3]}")


if __name__ == "__main__":
    main()
