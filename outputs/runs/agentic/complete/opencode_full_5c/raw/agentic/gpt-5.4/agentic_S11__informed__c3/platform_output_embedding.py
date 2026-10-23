from __future__ import annotations

from typing import Any, Dict, List

from model_client import get_azure_openai_client, get_embedding_deployment


def platform_output_embedding(text: str) -> Dict[str, Any]:
    client = get_azure_openai_client()
    deployment = get_embedding_deployment()
    response = client.embeddings.create(
        model=deployment,
        input=text,
    )
    item = response.data[0]
    vector: List[float] = list(item.embedding)
    return {
        "provider": "azure_openai",
        "model": deployment,
        "embedding": vector,
        "usage": response.usage.model_dump()
        if hasattr(response.usage, "model_dump")
        else {},
    }
