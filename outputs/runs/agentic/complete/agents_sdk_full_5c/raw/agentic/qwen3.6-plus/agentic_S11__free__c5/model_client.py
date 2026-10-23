"""
Local configuration and client helper utilities for Managed Model Platform Workflow.

Provides Azure OpenAI client configuration, endpoint resolution,
and utility functions for interacting with the Azure OpenAI managed model platform.
"""

import os
from typing import Optional

from openai import AzureOpenAI


def get_azure_openai_client(
    api_key: Optional[str] = None,
    azure_endpoint: Optional[str] = None,
    api_version: Optional[str] = None,
) -> AzureOpenAI:
    """
    Create and return a configured AzureOpenAI client instance.

    Resolves credentials from environment variables when not provided explicitly.

    Args:
        api_key: Azure OpenAI API key. Defaults to AZURE_OPENAI_API_KEY env var.
        azure_endpoint: Azure OpenAI resource endpoint. Defaults to AZURE_OPENAI_ENDPOINT env var.
        api_version: Azure OpenAI API version. Defaults to AZURE_OPENAI_API_VERSION env var.

    Returns:
        Configured AzureOpenAI client instance.
    """
    resolved_api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError(
            "Azure OpenAI API key not provided and AZURE_OPENAI_API_KEY env var not set"
        )

    resolved_endpoint = azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
    if not resolved_endpoint:
        raise ValueError(
            "Azure OpenAI endpoint not provided and AZURE_OPENAI_ENDPOINT env var not set"
        )

    resolved_api_version = api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")

    client = AzureOpenAI(
        api_key=resolved_api_key,
        azure_endpoint=resolved_endpoint,
        api_version=resolved_api_version,
    )
    return client


def get_deployment_endpoint(base_endpoint: str, deployment_name: str) -> str:
    """
    Construct the full deployment-scoped endpoint URL for an Azure OpenAI deployment.

    Args:
        base_endpoint: Base Azure OpenAI resource endpoint (e.g., https://myresource.openai.azure.com/)
        deployment_name: Name of the specific deployment.

    Returns:
        Full deployment endpoint URL.
    """
    base = base_endpoint.rstrip("/")
    return f"{base}/openai/deployments/{deployment_name}"


def normalize_system_prompt(system_prompt: Optional[str]) -> list[dict]:
    """
    Normalize a system prompt string into the messages format expected by Azure OpenAI.

    Args:
        system_prompt: Optional system prompt text.

    Returns:
        List of message dictionaries with system role if prompt provided.
    """
    if not system_prompt:
        return []
    return [{"role": "system", "content": system_prompt}]


def normalize_user_message(content: str) -> dict:
    """
    Create a user message dictionary for Azure OpenAI chat completions.

    Args:
        content: The user message content.

    Returns:
        Message dictionary with user role.
    """
    return {"role": "user", "content": content}


def build_messages(system_prompt: Optional[str], user_content: str) -> list[dict]:
    """
    Build the complete messages list for an Azure OpenAI chat completion request.

    Args:
        system_prompt: Optional system prompt.
        user_content: Required user message content.

    Returns:
        List of message dictionaries ready for API call.
    """
    messages = normalize_system_prompt(system_prompt)
    messages.append(normalize_user_message(user_content))
    return messages


def extract_text_from_completion(response) -> str:
    """
    Extract the text content from an Azure OpenAI chat completion response.

    Args:
        response: Azure OpenAI chat completion response object.

    Returns:
        Extracted text content from the first choice.
    """
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message.content or ""
    return ""


def extract_token_usage(response) -> dict:
    """
    Extract token usage information from an Azure OpenAI response.

    Args:
        response: Azure OpenAI response object with usage attribute.

    Returns:
        Dictionary with prompt_tokens, completion_tokens, and total_tokens.
    """
    usage = getattr(response, "usage", None)
    if usage:
        return {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }
    return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
