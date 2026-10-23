from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import EmbeddingVector
from select_platform_resource import select_platform_resource


def platform_output_embedding(text: str) -> EmbeddingVector:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="embedding")
    response = client.embeddings.create(
        model=resource.deployment_name or resource.model_id,
        input=text,
    )
    item = response.data[0]
    return EmbeddingVector(
        model=response.model,
        vector=item.embedding,
        dimensions=len(item.embedding),
        raw=response,
    )
