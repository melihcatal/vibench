import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PlatformResource:
    provider: str
    resource: str
    kind: str


def select_platform_resource(model_or_deployment: Optional[str] = None) -> PlatformResource:
    resource = model_or_deployment or os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    if "/" in resource and resource.count("/") >= 1:
        return PlatformResource(provider="openai", resource=resource, kind="model")
    if resource.startswith("gpt-") or resource.startswith("o-"):
        return PlatformResource(provider="openai", resource=resource, kind="model")
    if resource.startswith("azure:"):
        deployment = resource.split(":", 1)[1]
        if not deployment:
            raise ValueError("Azure deployment name is required")
        return PlatformResource(provider="azure-openai", resource=deployment, kind="deployment")
    if resource.startswith("openai:"):
        model = resource.split(":", 1)[1]
        if not model:
            raise ValueError("OpenAI model name is required")
        return PlatformResource(provider="openai", resource=model, kind="model")
    return PlatformResource(provider="openai", resource=resource, kind="model")


def resolve_before_invocation(model_or_deployment: Optional[str] = None) -> str:
    selected = select_platform_resource(model_or_deployment)
    if selected.provider == "azure-openai":
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required for Azure OpenAI")
        return f"{endpoint.rstrip('/')}/openai/deployments/{selected.resource}?api-version={api_version}"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI")
    return selected.resource
