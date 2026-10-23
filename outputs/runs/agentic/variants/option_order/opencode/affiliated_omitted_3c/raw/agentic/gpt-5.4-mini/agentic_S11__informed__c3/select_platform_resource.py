import os
from typing import Optional

from model_client import get_bedrock_client, platform_config


def select_platform_resource(preferred_model_id: Optional[str] = None) -> str:
    config = platform_config()
    candidate = preferred_model_id or config["model_id"]
    client = get_bedrock_client()
    response = client.list_foundation_models(byProvider="Anthropic")
    for model in response.get("modelSummaries", []):
        model_id = model.get("modelId")
        if model_id == candidate or candidate in (model_id or ""):
            return model_id
    return candidate
