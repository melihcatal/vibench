import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource_id: str
    resource_type: str


class ResourceResolutionError(ValueError):
    pass


def select_platform_resource(
    model: Optional[str] = None,
    deployment: Optional[str] = None,
    inference_resource: Optional[str] = None,
) -> PlatformResource:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_model = model or os.getenv("AZURE_OPENAI_MODEL") or "gpt-4.1-mini"
    azure_resource = inference_resource or os.getenv("AZURE_OPENAI_RESOURCE")

    if azure_deployment:
        return PlatformResource(
            provider="azure-openai",
            resource_id=azure_deployment,
            resource_type="deployment",
        )

    if azure_resource:
        return PlatformResource(
            provider="azure-openai",
            resource_id=azure_resource,
            resource_type="inference_resource",
        )

    if azure_endpoint:
        return PlatformResource(
            provider="azure-openai",
            resource_id=azure_model,
            resource_type="model",
        )

    raise ResourceResolutionError(
        "Unable to resolve a provider-specific resource. Set AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_RESOURCE, or AZURE_OPENAI_ENDPOINT."
    )
