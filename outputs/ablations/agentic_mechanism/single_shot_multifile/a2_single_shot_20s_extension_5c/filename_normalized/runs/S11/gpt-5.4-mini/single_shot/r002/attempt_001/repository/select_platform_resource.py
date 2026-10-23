import os
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name
from model_models import PlatformResource, ResourceSelection, normalize_resource_selection


def select_platform_resource(selection: Dict[str, Any] | ResourceSelection, client: Optional[OpenAI] = None) -> PlatformResource:
    normalized = normalize_resource_selection(selection)
    api_client = client or get_openai_client()
    model = get_model_name(normalized.model)
    api_client.responses.create(model=model, input=normalized.prompt, max_output_tokens=1)
    return PlatformResource(provider="openai", resource_id=model, model=model, metadata={"scope": normalized.scope})
