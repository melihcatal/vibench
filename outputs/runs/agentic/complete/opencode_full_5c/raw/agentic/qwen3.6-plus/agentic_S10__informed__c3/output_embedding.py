import os
from typing import Optional
from openai import OpenAI
from model_models import EmbeddingResult


def get_output_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> EmbeddingResult:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=key)

    kwargs = {
        "input": text,
        "model": model,
    }
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embedding = response.data[0].embedding
    actual_dimensions = len(embedding)

    return EmbeddingResult(
        embedding=embedding,
        model=response.model,
        dimensions=actual_dimensions,
    )
