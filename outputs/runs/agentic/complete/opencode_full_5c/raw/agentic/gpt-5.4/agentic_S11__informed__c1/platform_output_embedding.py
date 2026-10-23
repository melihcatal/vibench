from __future__ import annotations

from typing import Any, Dict

from model_client import create_platform_client, resolve_embedding_resource


def embed_platform_output(text: str) -> Dict[str, Any]:
    client = create_platform_client()
    deployment = resolve_embedding_resource()
    response = client.embeddings.create(
        model=deployment,
        input=text,
    )
    item = response.data[0]
    return {
        "provider": "azure_openai",
        "resource_id": deployment,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
        "usage": response.usage.model_dump()
        if hasattr(response.usage, "model_dump")
        else response.usage,
        "raw": response,
    }
