import os
from speech_client import get_openai_client
from speech_models import EmbeddingResult


def embed_script(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=dimensions,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        text=text,
        vector=vector,
        model=model,
        dimensions=len(vector),
    )
