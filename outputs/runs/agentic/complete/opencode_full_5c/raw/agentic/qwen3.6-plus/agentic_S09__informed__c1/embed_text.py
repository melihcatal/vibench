from typing import List, Optional
from openai import OpenAI
from embeddings_models import EmbeddingResponse, normalize_vector
from embeddings_client import create_openai_client, DEFAULT_MODEL


def embed_text(
    text: str,
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    normalize: bool = False,
    api_key: Optional[str] = None,
) -> EmbeddingResponse:
    client = create_openai_client(api_key)
    payload = {
        "model": model,
        "input": text,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    response = client.embeddings.create(**payload)
    embedding = response.data[0].embedding
    if normalize:
        embedding = normalize_vector(embedding)
    return EmbeddingResponse(
        embedding=embedding,
        model=response.model,
        usage_tokens=response.usage.total_tokens,
    )
