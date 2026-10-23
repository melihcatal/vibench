from typing import Optional

from model_client import create_platform_client, load_platform_config


# Provider-identifying signal: OpenAI Responses API / model names like gpt-4.1-mini.
def select_platform_resource(preferred_model: Optional[str] = None) -> str:
    config = load_platform_config()
    client = create_platform_client()
    models = client.models.list()
    chosen = preferred_model or config.model
    for item in models.data:
        if getattr(item, "id", None) == chosen:
            return item.id
    return chosen
