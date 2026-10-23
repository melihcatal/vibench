from __future__ import annotations

from model_client import get_default_platform_resource
from model_models import PlatformResource


def select_platform_resource(task: str = "chat", preferred_region: str | None = None) -> PlatformResource:
    resource = get_default_platform_resource(task=task)
    if preferred_region:
        resource.region = preferred_region
        resource.metadata["azure_region"] = preferred_region
    resource.metadata["provider"] = "azure_openai"
    resource.metadata["azure_deployment"] = resource.deployment_name
    return resource
