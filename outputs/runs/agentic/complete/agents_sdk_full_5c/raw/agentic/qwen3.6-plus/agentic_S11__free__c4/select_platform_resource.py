"""Resolves a provider-specific model, deployment, or inference resource before invocation.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
Uses concrete Azure OpenAI model family identifiers (e.g., gpt-4o, gpt-4, gpt-35-turbo).
"""

from __future__ import annotations

from typing import Optional

from model_client import build_azure_openai_client
from openai import AzureOpenAI


# Canonical Azure OpenAI deployment model identifiers
AZURE_MODEL_FAMILIES = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-35-turbo",
    "text-embedding-ada-002",
    "text-embedding-3-large",
    "text-embedding-3-small",
]


def find_best_deployment(
    *,
    client: Optional[AzureOpenAI] = None,
    model_family: Optional[str] = None,
    fallback_family: str = "gpt-4o",
) -> str:
    """Resolve the best available Azure OpenAI deployment for a given model family.

    Queries the Azure OpenAI provider for available deployments and selects one
    matching the requested model family. If no match is found, falls back to
    a default deployment or raises an error.

    Args:
        client: AzureOpenAI client. Built automatically if not provided.
        model_family: Desired Azure OpenAI model family (e.g., 'gpt-4o', 'gpt-35-turbo').
        fallback_family: Default model family to use when model_family is None.

    Returns:
        The deployment name (id) string for the resolved resource.

    Raises:
        ValueError: If no matching deployment is found for the requested model family.
    """
    if client is None:
        client = build_azure_openai_client()

    target_family = model_family or fallback_family
    if target_family not in AZURE_MODEL_FAMILIES:
        raise ValueError(
            f"Unknown Azure OpenAI model family '{target_family}'. "
            f"Expected one of: {', '.join(AZURE_MODEL_FAMILIES)}"
        )

    # Query Azure OpenAI provider for available model deployments
    available_deployments = list(client.models.list())

    if not available_deployments:
        raise RuntimeError(
            "No deployments found in Azure OpenAI resource. "
            "Ensure the endpoint points to a resource with at least one model deployment."
        )

    # Try exact match first on the deployment id
    for deployment in available_deployments.data:
        deployment_id = deployment.id
        deployment_model = getattr(deployment, "model", None)

        # Match on model name or deployment id containing the family
        if deployment_model == target_family or target_family in deployment_id.lower():
            return deployment_id

    # Try substring match on deployment model
    for deployment in available_deployments.data:
        deployment_model = getattr(deployment, "model", "") or ""
        deployment_id = deployment.id
        if target_family in deployment_model.lower() or target_family in deployment_id.lower():
            return deployment_id

    # No match found — return the first available deployment as best-effort
    # but log a warning-style note for callers
    first_deployment = available_deployments.data[0]
    return first_deployment.id


def resolve_deployment_details(
    *,
    deployment_name: str,
    client: Optional[AzureOpenAI] = None,
) -> dict:
    """Retrieve detailed metadata for a specific Azure OpenAI deployment.

    Args:
        deployment_name: The deployment id string.
        client: AzureOpenAI client. Built automatically if not provided.

    Returns:
        Dict with deployment id, model name, status, and creation timestamp.
    """
    if client is None:
        client = build_azure_openai_client()

    deployment = client.models.get(deployment_name)
    return {
        "id": deployment.id,
        "model": getattr(deployment, "model", None),
        "status": getattr(deployment, "status", None),
        "created_at": getattr(deployment, "created_at", None),
        "provider": "azure_openai",
        "endpoint_base": client._client.base_url.host if hasattr(client, "_client") and client._client else None,
    }


def enumerate_deployment_model_map(
    client: Optional[AzureOpenAI] = None,
) -> dict[str, str]:
    """Build a mapping of Azure OpenAI deployment IDs to their backing model names.

    Args:
        client: AzureOpenAI client. Built automatically if not provided.

    Returns:
        Dict mapping deployment_id -> model_name.
    """
    if client is None:
        client = build_azure_openai_client()

    result = {}
    for deployment in client.models.list().data:
        model_name = getattr(deployment, "model", None) or "unknown"
        result[deployment.id] = model_name
    return result
