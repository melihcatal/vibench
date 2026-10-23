"""Local configuration and client helper utilities for Managed Model Platform Workflow.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
"""

import os
from typing import Optional

from openai import AzureOpenAI


# Azure OpenAI provider-specific defaults
_AZURE_OPENAI_ENDPOINT_ENV = "AZURE_OPENAI_ENDPOINT"
_AZURE_OPENAI_API_KEY_ENV = "AZURE_OPENAI_API_KEY"
_AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
_AZURE_OPENAI_TIMEOUT = float(os.environ.get("AZURE_OPENAI_TIMEOUT", "60.0"))
_AZURE_OPENAI_MAX_RETRIES = int(os.environ.get("AZURE_OPENAI_MAX_RETRIES", "3"))


def resolve_azure_endpoint() -> str:
    """Return the Azure OpenAI resource endpoint from environment."""
    endpoint = os.environ.get(_AZURE_OPENAI_ENDPOINT_ENV)
    if not endpoint:
        raise RuntimeError(
            f"Missing required provider environment variable: {_AZURE_OPENAI_ENDPOINT_ENV}. "
            f"Expected format: https://<resource-name>.openai.azure.com/"
        )
    if not endpoint.rstrip("/").endswith(".openai.azure.com"):
        raise ValueError(
            f"Invalid Azure OpenAI endpoint '{endpoint}'. "
            f"Must be an *.openai.azure.com resource URL."
        )
    return endpoint.rstrip("/")


def resolve_azure_api_key() -> str:
    """Return the Azure OpenAI API key from environment."""
    key = os.environ.get(_AZURE_OPENAI_API_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"Missing required provider environment variable: {_AZURE_OPENAI_API_KEY_ENV}"
        )
    return key


def build_azure_openai_client(
    *,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None,
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
) -> AzureOpenAI:
    """Build a provider-specific AzureOpenAI client with resolved configuration.

    Args:
        endpoint: Azure resource endpoint (default: from AZURE_OPENAI_ENDPOINT).
        api_key: Azure API key (default: from AZURE_OPENAI_API_KEY).
        api_version: Azure OpenAI API version (default: AZURE_OPENAI_API_VERSION env or 2024-02-01).
        timeout: Request timeout in seconds.
        max_retries: Number of retry attempts.

    Returns:
        Configured AzureOpenAI client instance.
    """
    resolved_endpoint = endpoint or resolve_azure_endpoint()
    resolved_key = api_key or resolve_azure_api_key()
    resolved_api_version = api_version or _AZURE_OPENAI_API_VERSION
    resolved_timeout = timeout if timeout is not None else _AZURE_OPENAI_TIMEOUT
    resolved_retries = max_retries if max_retries is not None else _AZURE_OPENAI_MAX_RETRIES

    client = AzureOpenAI(
        azure_endpoint=resolved_endpoint,
        api_key=resolved_key,
        api_version=resolved_api_version,
        timeout=resolved_timeout,
        max_retries=resolved_retries,
    )
    return client


def list_available_deployments(
    client: AzureOpenAI,
) -> list[dict]:
    """List deployment resources from the Azure OpenAI provider.

    Args:
        client: AzureOpenAI client instance.

    Returns:
        List of deployment dicts with id, model, and status.
    """
    deployments = client.models.list()
    result = []
    for deployment in deployments.data:
        result.append({
            "id": deployment.id,
            "model": getattr(deployment, "model", None),
            "status": getattr(deployment, "status", None),
            "created_at": getattr(deployment, "created_at", None),
        })
    return result


def build_chat_payload(
    *,
    deployment: str,
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stream: bool = False,
) -> dict:
    """Normalize a chat completion request payload for Azure OpenAI.

    Args:
        deployment: Azure OpenAI deployment name (resource-scoped).
        messages: List of message dicts with 'role' and 'content'.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        top_p: Nucleus sampling parameter.
        frequency_penalty: Frequency penalty.
        presence_penalty: Presence penalty.
        stream: Whether to stream the response.

    Returns:
        Normalized payload dict ready for the Azure OpenAI chat completions API.
    """
    return {
        "deployment_id": deployment,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stream": stream,
    }
