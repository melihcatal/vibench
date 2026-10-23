from __future__ import annotations

from model_client import get_azure_openai_client, get_embedding_deployment
from model_models import EmbeddingResult



def platform_output_embedding(text: str) -> EmbeddingResult:
    client = get_azure_openai_client()
    deployment = get_embedding_deployment()
    response = client.embeddings.create(
        model=deployment,
        input=text,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        model=deployment,
        dimensions=len(vector),
        raw=response,
    )
