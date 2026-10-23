"""Resolve a provider-specific model, deployment, or inference resource before invocation.

Uses Azure OpenAI Service (sdk=openai) with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY.
"""

import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI

from model_client import create_azure_openai_client


@dataclass
class ResolvedResource:
    """Resolved Azure OpenAI deployment resource."""

    deployment_name: str
    model_family: str
    endpoint: str
    api_version: str
    resource_id: str
    region: str


_KNOWN_DEPLOYMENT_MODELS: dict[str, str] = {
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4": "gpt-4",
    "gpt-35-turbo": "gpt-3.5-turbo",
    "gpt-35-turbo-16k": "gpt-3.5-turbo-16k",
    "text-embedding-ada-002": "text-embedding-ada-002",
    "text-embedding-3-small": "text-embedding-3-small",
    "text-embedding-3-large": "text-embedding-3-large",
}


def _resolve_model_family(deployment_name: str) -> str:
    """Map an Azure OpenAI deployment name to its underlying model family."""
    return _KNOWN_DEPLOYMENT_MODELS.get(
        deployment_name, deployment_name
    )


def _extract_resource_info_from_endpoint(endpoint: str) -> dict:
    """Extract region and resource ID hints from the Azure OpenAI endpoint URL.

    Example endpoint: https://myresource.openai.azure.com
    """
    hostname = endpoint.replace("https://", "").rstrip("/")
    parts = hostname.split(".")
    resource_name = parts[0] if parts else ""
    region = ""
    for part in parts:
        if part in (
            "eastus",
            "westus",
            "westus2",
            "westus3",
            "centralus",
            "northcentralus",
            "southcentralus",
            "eastus2",
            "southeastasia",
            "northeurope",
            "westeurope",
            "uksouth",
            "australiaeast",
            "japaneast",
        ):
            region = part
            break
    return {"resource_name": resource_name, "region": region}


def list_available_deployments(
    client: Optional[AzureOpenAI] = None,
) -> list[str]:
    """List known deployment names from environment configuration or a preset registry."""
    env_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    deployments = []
    if env_deployment:
        deployments.append(env_deployment)
    return deployments


def select_platform_resource(
    deployment_name: Optional[str] = None,
    client: Optional[AzureOpenAI] = None,
) -> ResolvedResource:
    """Resolve an Azure OpenAI deployment resource before invocation.

    Uses the AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT environment
    variables to identify the target model deployment, then returns a
    ResolvedResource with provider metadata.

    Args:
        deployment_name: Override deployment name. Defaults to AZURE_OPENAI_DEPLOYMENT or "gpt-4o".
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        ResolvedResource with resolved deployment and model information.
    """
    resolved_client = client or create_azure_openai_client()
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-01-preview")
    resolved_deployment = deployment_name or os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    model_family = _resolve_model_family(resolved_deployment)
    info = _extract_resource_info_from_endpoint(endpoint)
    resource_id = f"/subscriptions/azure-openai/{info['resource_name']}/deployments/{resolved_deployment}"

    return ResolvedResource(
        deployment_name=resolved_deployment,
        model_family=model_family,
        endpoint=endpoint,
        api_version=api_version,
        resource_id=resource_id,
        region=info.get("region", "unknown"),
    )


if __name__ == "__main__":
    resource = select_platform_resource()
    print(f"Resolved deployment: {resource.deployment_name}")
    print(f"Model family: {resource.model_family}")
    print(f"Endpoint: {resource.endpoint}")
    print(f"Resource ID: {resource.resource_id}")
    print(f"Region: {resource.region}")
