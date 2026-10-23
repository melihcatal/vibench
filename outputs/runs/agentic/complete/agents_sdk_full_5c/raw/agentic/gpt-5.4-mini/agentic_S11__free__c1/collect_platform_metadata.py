from __future__ import annotations

from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_client
from model_models import PlatformResponse, normalize_text
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str, resource_id: Optional[str] = None, client: Optional[OpenAI] = None) -> Dict[str, Any]:
    client = client or get_client()
    model = select_platform_resource(resource_id, client=client)
    response = client.responses.create(model=model, input=prompt)
    return {
        "response": PlatformResponse(
            text=normalize_text(getattr(response, "output_text", None) or response.output),
            model=model,
            resource_id=resource_id,
            usage=getattr(response, "usage", None),
            raw=response,
        ),
        "provider": "openai",
        "model": model,
        "response_id": getattr(response, "id", None),
        "usage": getattr(response, "usage", None),
        "project": getattr(client, "project", None),
    }
