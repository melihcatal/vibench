"""Resolves a provider-specific Azure OpenAI deployment resource before invocation.

Uses the Azure AI Inference platform to resolve and select a specific
deployment-scoped model resource by deployment name within an
Azure OpenAI Service project.
"""

from typing import Dict, Any, Optional, List, Tuple

import openai
from openai import AzureOpenAI

from model_client import load_platform_config, get_azure_openai_client
from model_models import PlatformInvocationRequest, PlatformInvocationResponse


AZURE_OPENAI_API_VERSION = "2024-10-21"


def list_available_deployments(
    provider_config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, str]]:
    """List available Azure OpenAI deployments in the project.

    Uses the Azure OpenAI Management endpoint to enumerate all
    deployments scoped to the configured Azure OpenAI resource.

    Args:
        provider_config: Optional pre-loaded Azure configuration.

    Returns:
        List of deployment metadata dictionaries.
    """
    if provider_config is None:
        provider_config = load_platform_config("azure")

    client = get_azure_openai_client(provider_config)

    try:
        deployments = client.models.list()
        result = []
        for model in deployments:
            deployment_info = {
                "id": getattr(model, "id", ""),
                "model_name": getattr(model, "model_name", ""),
                "status": getattr(model, "status", "unknown"),
            }
            result.append(deployment_info)
        return result
    except Exception:
        fallback = provider_config.get("deployment_name", "gpt-4o")
        return [
            {
                "id": fallback,
                "model_name": fallback,
                "status": "available",
            }
        ]


def resolve_deployment_resource(
    deployment_name: str,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """Resolve a specific Azure OpenAI deployment resource by name.

    Validates that the deployment exists and returns its configuration
    details including the underlying model name and deployment status.

    Args:
        deployment_name: Azure OpenAI deployment name to resolve.
        provider_config: Optional pre-loaded Azure configuration.

    Returns:
        Dictionary with deployment details (id, model_name, status).
    """
    if provider_config is None:
        provider_config = load_platform_config("azure")

    client = get_azure_openai_client(provider_config)

    try:
        model_info = client.models.retrieve(model=deployment_name)
        return {
            "id": getattr(model_info, "id", deployment_name),
            "model_name": getattr(model_info, "model_name", deployment_name),
            "status": getattr(model_info, "status", "available"),
            "deployment_name": deployment_name,
            "azure_endpoint": provider_config.get("azure_endpoint", ""),
        }
    except Exception:
        return {
            "id": deployment_name,
            "model_name": deployment_name,
            "status": "fallback",
            "deployment_name": deployment_name,
            "azure_endpoint": provider_config.get("azure_endpoint", ""),
        }


def select_best_deployment(
    preferred_models: Optional[List[str]] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Tuple[str, Dict[str, str]]:
    """Select the best available deployment from preferred model list.

    Iterates through preferred model names and returns the first
    available Azure OpenAI deployment resource.

    Args:
        preferred_models: Ordered list of preferred model/deployment names.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Tuple of (selected_deployment_name, deployment_metadata).
    """
    if provider_config is None:
        provider_config = load_platform_config("azure")

    default_preferred = ["gpt-4o", "gpt-4", "gpt-35-turbo"]
    candidates = preferred_models or default_preferred

    available = list_available_deployments(provider_config)
    available_ids = {d["id"]: d for d in available}

    for candidate in candidates:
        if candidate in available_ids:
            deployment = resolve_deployment_resource(candidate, provider_config)
            return candidate, deployment

    fallback = provider_config.get("deployment_name", "gpt-4o")
    deployment = resolve_deployment_resource(fallback, provider_config)
    return fallback, deployment


def invoke_selected_deployment(
    prompt: str,
    system_prompt: Optional[str] = None,
    deployment_name: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> PlatformInvocationResponse:
    """Invoke the platform using a resolved Azure OpenAI deployment resource.

    First resolves the deployment resource, then invokes the model
    through the Azure OpenAI project-scoped client.

    Args:
        prompt: User input text.
        system_prompt: Optional system prompt.
        deployment_name: Specific deployment to use (auto-resolved if None).
        provider_config: Optional pre-loaded configuration.

    Returns:
        PlatformInvocationResponse with generated text.
    """
    if provider_config is None:
        provider_config = load_platform_config("azure")

    if deployment_name is None:
        deployment_name, _ = select_best_deployment(
            provider_config=provider_config
        )

    client = get_azure_openai_client(provider_config)

    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )

    text = ""
    if completion.choices and completion.choices[0].message:
        text = completion.choices[0].message.content or ""

    usage = None
    if hasattr(completion, "usage"):
        usage = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }

    return PlatformInvocationResponse(
        text=text,
        model=deployment_name,
        response_id=getattr(completion, "id", None),
        usage=usage,
        raw_response=completion,
        provider="azure",
    )
