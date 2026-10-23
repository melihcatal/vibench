from __future__ import annotations

import os

from model_client import load_default_resource
from model_models import ResourceSelection


SUPPORTED_AZURE_MODELS = {
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "gpt-4o": "gpt-4o",
}


def select_platform_resource(preferred_model: str | None = None) -> ResourceSelection:
    resource = load_default_resource()
    requested = preferred_model or os.getenv("AZURE_OPENAI_CHAT_MODEL", resource.model)
    if requested in SUPPORTED_AZURE_MODELS:
        resource.model = SUPPORTED_AZURE_MODELS[requested]
    deployment_override = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    if deployment_override:
        resource.deployment_name = deployment_override
    elif requested in SUPPORTED_AZURE_MODELS:
        resource.deployment_name = requested
    return resource
