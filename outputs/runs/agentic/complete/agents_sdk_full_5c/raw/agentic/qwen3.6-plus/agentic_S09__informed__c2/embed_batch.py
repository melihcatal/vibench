"""
Same-scenario: Generate embeddings for a batch of texts.
Provider: OpenAI Embeddings API via openai SDK.
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

from typing import List, Optional

from openai import OpenAI

from embeddings_client import create_embeddings_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import EmbeddingRequest, EmbeddingResponse, parse_openai_embedding_response


def embed_batch(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    batch_size: int = 100,
) -> List[EmbeddingResponse]:
    """Generate embeddings for a batch of texts using OpenAI.

    OpenAI's embeddings endpoint accepts up to 2048 inputs per request;
    this function respects the provided batch_size limit.

    Args:
        texts: List of input text strings.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: Optional override for OPENAI_API_KEY.
        batch_size: Maximum texts per API call.

    Returns:
        List of EmbeddingResponse objects, one per input text.
    """
    resolved_model = model or DEFAULT_EMBEDDING_MODEL
    client = create_embeddings_client(api_key=api_key)

    all_responses: List[EmbeddingResponse] = []

    for start in range(0, len(texts), batch_size):
        chunk = texts[start : start + batch_size]
        request_kwargs = {
            "input": chunk,
            "model": resolved_model,
            "encoding_format": "float",
        }
        if dimensions is not None:
            request_kwargs["dimensions"] = dimensions

        raw_response = client.embeddings.create(**request_kwargs)

        for idx in range(len(chunk)):
            resp = parse_openai_embedding_response(raw_response, index=idx)
            all_responses.append(resp)

    return all_responses


if __name__ == "__main__":
    batch = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is a subset of artificial intelligence.",
        "Embeddings represent text as dense vectors.",
    ]
    results = embed_batch(batch)
    for i, r in enumerate(results):
        print(f"Text {i}: model={r.model}, dims={len(r.embedding)}, tokens={r.usage_tokens}")
