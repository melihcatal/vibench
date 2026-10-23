import os
from typing import List, Optional
from openai import OpenAI
from speech_models import EmbeddingRequest, EmbeddingResponse


def embed_script(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> EmbeddingResponse:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    client = OpenAI(api_key=key)
    params = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    embedding_data = response.data[0]
    return EmbeddingResponse(
        embedding=embedding_data.embedding,
        model=embedding_data.model,
        usage_tokens=response.usage.total_tokens,
    )


def embed_script_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[EmbeddingResponse]:
    responses = []
    for text in texts:
        responses.append(
            embed_script(
                text,
                model=model,
                dimensions=dimensions,
                api_key=api_key,
            )
        )
    return responses
