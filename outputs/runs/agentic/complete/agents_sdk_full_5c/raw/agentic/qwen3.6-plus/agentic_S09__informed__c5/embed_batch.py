"""
[SAME-SCENARIO] Generates embeddings for a batch of texts.
Provider: OpenAI Embeddings API (text-embedding-3-small)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import List, Optional, Dict

from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import (
    EmbeddingResult,
    EmbeddingBatchResponse,
    normalize_vector,
    build_embedding_request,
    parse_openai_response,
)


def embed_batch(
    texts: List[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    normalize: bool = True,
    dimensions: Optional[int] = None,
    batch_size: int = 100,
) -> EmbeddingBatchResponse:
    """
    Generate embedding vectors for a batch of texts using OpenAI.

    Args:
        texts: List of input strings to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).
        normalize: Whether to L2-normalize each returned vector.
        dimensions: Optional output dimensionality for embeddings.
        batch_size: Maximum texts per API call (OpenAI supports up to 2048).

    Returns:
        EmbeddingBatchResponse containing all embedding results.
    """
    client = get_openai_client(api_key=api_key)
    model_name = model or get_embedding_model()

    all_results: List[EmbeddingResult] = []
    total_tokens = 0

    for i in range(0, len(texts), batch_size):
        chunk = texts[i : i + batch_size]

        request = build_embedding_request(
            texts=chunk,
            model=model_name,
            dimensions=dimensions,
        )

        response = client.embeddings.create(
            model=request.model,
            input=request.input_texts,
            encoding_format="float",
            dimensions=dimensions,
        )

        usage = getattr(response, "usage", None)
        if usage:
            total_tokens += usage.total_tokens

        for item in response.data:
            vec = item.embedding
            if normalize:
                vec = normalize_vector(vec)
            all_results.append(
                EmbeddingResult(
                    text=chunk[item.index],
                    vector=vec,
                    index=i + item.index,
                    model=model_name,
                )
            )

    return EmbeddingBatchResponse(
        results=all_results,
        model=model_name,
        total_tokens=total_tokens,
    )


if __name__ == "__main__":
    sample_texts = [
        "OpenAI provides embedding models.",
        "Cosine similarity measures vector alignment.",
        "Batch processing improves throughput.",
    ]
    batch_response = embed_batch(sample_texts)
    print(f"Model: {batch_response.model}")
    print(f"Total tokens used: {batch_response.total_tokens}")
    print(f"Embeddings generated: {len(batch_response.results)}")
    for r in batch_response.results:
        print(f"  [{r.index}] dim={len(r.vector)} text={r.text[:40]}...")
