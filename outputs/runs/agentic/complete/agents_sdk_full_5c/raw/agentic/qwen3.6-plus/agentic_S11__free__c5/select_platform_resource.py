"""
[SAME-SCENARIO] Resolves a provider-specific model, deployment, or inference resource
before invocation on the Azure OpenAI managed model platform.

Uses the Azure OpenAI management / model catalog to resolve deployment names,
model identifiers, and validate resource availability prior to invocation.
"""

from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI

from model_models import PlatformModelRequest
from model_client import get_azure_openai_client


# Supported Azure OpenAI model families and their deployment naming conventions
AZURE_OPENAI_MODEL_REGISTRY: dict[str, dict] = {
    "gpt-4o": {
        "model_name": "gpt-4o",
        "model_version": "2024-05-13",
        "capabilities": ["chat", "vision", "function_calling"],
        "max_tokens": 4096,
        "deployment_name_hint": "gpt-4o",
    },
    "gpt-4o-mini": {
        "model_name": "gpt-4o-mini",
        "model_version": "2024-07-18",
        "capabilities": ["chat", "function_calling"],
        "max_tokens": 4096,
        "deployment_name_hint": "gpt-4o-mini",
    },
    "gpt-35-turbo": {
        "model_name": "gpt-35-turbo",
        "model_version": "0125",
        "capabilities": ["chat", "function_calling"],
        "max_tokens": 4096,
        "deployment_name_hint": "gpt-35-turbo",
    },
    "gpt-4": {
        "model_name": "gpt-4",
        "model_version": "turbo-2024-04-09",
        "capabilities": ["chat", "function_calling"],
        "max_tokens": 4096,
        "deployment_name_hint": "gpt-4",
    },
    "text-embedding-ada-002": {
        "model_name": "text-embedding-ada-002",
        "model_version": "2",
        "capabilities": ["embeddings"],
        "max_tokens": 8191,
        "deployment_name_hint": "text-embedding-ada-002",
    },
    "text-embedding-3-large": {
        "model_name": "text-embedding-3-large",
        "model_version": "1",
        "capabilities": ["embeddings"],
        "max_tokens": 8191,
        "deployment_name_hint": "text-embedding-3-large",
    },
    "text-embedding-3-small": {
        "model_name": "text-embedding-3-small",
        "model_version": "1",
        "capabilities": ["embeddings"],
        "max_tokens": 8191,
        "deployment_name_hint": "text-embedding-3-small",
    },
    "tts-1": {
        "model_name": "tts-1",
        "model_version": "1",
        "capabilities": ["speech"],
        "max_tokens": None,
        "deployment_name_hint": "tts-1",
    },
    "tts-1-hd": {
        "model_name": "tts-1-hd",
        "model_version": "1",
        "capabilities": ["speech"],
        "max_tokens": None,
        "deployment_name_hint": "tts-1-hd",
    },
}


class ResourceNotFoundError(Exception):
    """Raised when a requested Azure OpenAI deployment or model cannot be resolved."""


def resolve_model_config(
    model_key: str,
    registry: Optional[dict] = None,
) -> dict:
    """
    Resolve Azure OpenAI model configuration from the provider-specific registry.

    Args:
        model_key: Model key to look up (e.g., 'gpt-4o', 'gpt-35-turbo').
        registry: Optional custom registry dict. Defaults to AZURE_OPENAI_MODEL_REGISTRY.

    Returns:
        Model configuration dictionary with model_name, version, capabilities, etc.

    Raises:
        ResourceNotFoundError: If the model key is not found in the registry.
    """
    lookup_registry = registry if registry is not None else AZURE_OPENAI_MODEL_REGISTRY
    if model_key not in lookup_registry:
        raise ResourceNotFoundError(
            f"Model '{model_key}' not found in Azure OpenAI model registry. "
            f"Available models: {', '.join(lookup_registry.keys())}"
        )
    return lookup_registry[model_key]


def resolve_deployment_for_request(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> tuple[str, dict]:
    """
    Resolve the Azure OpenAI deployment name and model config for a given request.

    If the request already specifies a deployment_name, validates it against
    the Azure OpenAI model registry. If not, resolves from registry using
    a model key derived from the deployment name.

    Args:
        request: PlatformModelRequest with deployment_name set.
        client: Optional AzureOpenAI client for runtime validation.

    Returns:
        Tuple of (resolved_deployment_name, model_config_dict).

    Raises:
        ResourceNotFoundError: If the deployment cannot be resolved.
    """
    deployment_name = request.deployment_name

    # Try exact match in registry first
    if deployment_name in AZURE_OPENAI_MODEL_REGISTRY:
        model_config = AZURE_OPENAI_MODEL_REGISTRY[deployment_name]
        return deployment_name, model_config

    # Try finding a registry key that matches deployment_name
    for key, config in AZURE_OPENAI_MODEL_REGISTRY.items():
        if config["deployment_name_hint"] == deployment_name:
            return deployment_name, config

    # Attempt to validate deployment against Azure OpenAI via the API
    if client is not None:
        try:
            # List models to check if deployment exists on the Azure resource
            models = client.models.list()
            for model in models.data:
                if model.id == deployment_name or deployment_name in model.id:
                    fallback_config = {
                        "model_name": deployment_name,
                        "model_version": "unknown",
                        "capabilities": ["chat"],
                        "max_tokens": request.max_tokens or 4096,
                        "deployment_name_hint": deployment_name,
                    }
                    return deployment_name, fallback_config
        except Exception:
            pass

    # Return with best-effort config if no exact match
    best_effort_config = {
        "model_name": deployment_name,
        "model_version": "unknown",
        "capabilities": ["chat"],
        "max_tokens": request.max_tokens or 4096,
        "deployment_name_hint": deployment_name,
    }
    return deployment_name, best_effort_config


def get_available_models(
    client: Optional[AzureOpenAI] = None,
) -> list[dict]:
    """
    Retrieve available Azure OpenAI models and deployments from the provider.

    Args:
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        List of available model dictionaries with id, object type, and owned_by.
    """
    if client is None:
        client = get_azure_openai_client()

    models_response = client.models.list()
    available = []
    for model in models_response.data:
        available.append({
            "id": model.id,
            "object": model.object,
            "owned_by": model.owned_by,
        })
    return available


def validate_deployment_exists(
    deployment_name: str,
    client: Optional[AzureOpenAI] = None,
) -> bool:
    """
    Validate that a deployment exists on the Azure OpenAI resource.

    Args:
        deployment_name: Azure OpenAI deployment name to validate.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        True if deployment is found, False otherwise.
    """
    if client is None:
        client = get_azure_openai_client()

    try:
        models = client.models.list()
        for model in models.data:
            if deployment_name in model.id:
                return True
    except Exception:
        pass
    return False


def select_resource_by_capability(
    required_capabilities: list[str],
    client: Optional[AzureOpenAI] = None,
) -> Optional[tuple[str, dict]]:
    """
    Select an Azure OpenAI deployment that supports the required capabilities.

    Args:
        required_capabilities: List of capability names (e.g., ['chat', 'vision']).
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        Tuple of (deployment_name, model_config) or None if no match found.
    """
    for key, config in AZURE_OPENAI_MODEL_REGISTRY.items():
        model_caps = set(config.get("capabilities", []))
        required = set(required_capabilities)
        if required.issubset(model_caps):
            return config["deployment_name_hint"], config
    return None
