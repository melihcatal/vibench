from typing import List, Optional
from openai import OpenAI
from embeddings_models import BatchEmbeddingResponse, normalize_vector
from embeddings_client import create_openai_client, DEFAULT_MODEL


def embed_batch(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    normalize: bool = False,
    api_key: Optional[str] = None,
) -> BatchEmbeddingResponse:
    client = create_openai_client(api_key)
    payload = {
        "model": model,
        "input": texts,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    response = client.embeddings.create(**payload)
    embeddings = [item.embedding for item in response.data]
    if normalize:
        embeddings = [normalize_vector(emb) for emb in embeddings]
    return BatchEmbeddingResponse(
        embeddings=embeddings,
        models=[response.model] * len(embeddings),
        usage_tokens=response.usage.total_tokens,
    )
