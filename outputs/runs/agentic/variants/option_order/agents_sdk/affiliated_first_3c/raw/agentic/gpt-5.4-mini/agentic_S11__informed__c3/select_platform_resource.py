from __future__ import annotations

from typing import Any, Dict

from openai import AzureOpenAI

from model_client import load_settings
from model_models import PlatformResource


def select_platform_resource(preferred_model: str | None = None) -> PlatformResource:
    settings = load_settings()
    client = AzureOpenAI(azure_endpoint=settings.endpoint, api_key=settings.api_key, api_version=settings.api_version)
    models = client.models.list()
    chosen = preferred_model or settings.deployment
    resource_id = chosen
    for item in getattr(models, "data", []) or []:
        if getattr(item, "id", None) == chosen:
            resource_id = item.id
            break
    return PlatformResource(provider="azure-openai", resource_id=resource_id, model=chosen, client_hint="AzureOpenAI")
