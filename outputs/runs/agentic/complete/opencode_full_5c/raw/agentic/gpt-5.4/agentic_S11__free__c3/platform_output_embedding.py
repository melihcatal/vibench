from typing import Any, Dict, List

from model_client import get_client
from select_platform_resource import select_platform_resource


def platform_output_embedding(text: str) -> Dict[str, Any]:
    resource = select_platform_resource("embedding")
    client = get_client()
    response = client.embeddings.create(
        model=resource["resource_id"],
        input=text,
    )
    item = response.data[0]
    return {
        "provider": "openai",
        "model": resource["resource_id"],
        "embedding": list(item.embedding),
        "dimensions": len(item.embedding),
        "usage": response.usage.model_dump()
        if hasattr(response.usage, "model_dump")
        else response.usage,
        "provider_response": response,
    }
