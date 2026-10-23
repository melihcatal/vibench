"""Local configuration and client helper utilities for Managed Model Platform Workflow.

Provides centralized configuration loading, client initialization,
and shared utilities for interacting with managed model providers.
"""

import os
from typing import Any, Dict, Optional

import openai
from openai import OpenAI


def load_platform_config(provider: str = "openai") -> Dict[str, Any]:
    """Load platform configuration from environment variables.

    Args:
        provider: Provider identifier (e.g., "openai", "azure", "anthropic").

    Returns:
        Dictionary of provider-specific configuration values.
    """
    config: Dict[str, Any] = {"provider": provider}

    if provider == "openai":
        config["api_key"] = os.environ.get("OPENAI_API_KEY", "")
        config["base_url"] = os.environ.get("OPENAI_BASE_URL", None)
        config["default_model"] = os.environ.get(
            "OPENAI_DEFAULT_MODEL", "gpt-4o-2024-08-06"
        )
        config["embedding_model"] = os.environ.get(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )
        config["tts_model"] = os.environ.get("OPENAI_TTS_MODEL", "tts-1-hd")
        config["tts_voice"] = os.environ.get("OPENAI_TTS_VOICE", "alloy")
    elif provider == "azure":
        config["api_key"] = os.environ.get("AZURE_OPENAI_API_KEY", "")
        config["azure_endpoint"] = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        config["api_version"] = os.environ.get(
            "AZURE_OPENAI_API_VERSION", "2024-10-21"
        )
        config["deployment_name"] = os.environ.get(
            "AZURE_OPENAI_DEPLOYMENT", "gpt-4o"
        )
    elif provider == "anthropic":
        config["api_key"] = os.environ.get("ANTHROPIC_API_KEY", "")
        config["default_model"] = os.environ.get(
            "ANTHROPIC_DEFAULT_MODEL", "claude-3-5-sonnet-20241022"
        )

    return config


def get_openai_client(provider_config: Optional[Dict[str, Any]] = None) -> OpenAI:
    """Create and return an OpenAI SDK client with loaded configuration.

    Args:
        provider_config: Optional pre-loaded configuration dictionary.
            If not provided, configuration is loaded from environment.

    Returns:
        Configured OpenAI client instance.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    client_kwargs: Dict[str, Any] = {
        "api_key": provider_config["api_key"],
    }

    base_url = provider_config.get("base_url")
    if base_url:
        client_kwargs["base_url"] = base_url

    return openai.OpenAI(**client_kwargs)


def get_azure_openai_client(
    provider_config: Optional[Dict[str, Any]] = None,
) -> openai.AzureOpenAI:
    """Create and return an Azure OpenAI SDK client.

    Args:
        provider_config: Optional pre-loaded configuration dictionary.

    Returns:
        Configured AzureOpenAI client instance.
    """
    if provider_config is None:
        provider_config = load_platform_config("azure")

    return openai.AzureOpenAI(
        api_key=provider_config["api_key"],
        azure_endpoint=provider_config["azure_endpoint"],
        api_version=provider_config["api_version"],
    )


def get_anthropic_client(provider_config: Optional[Dict[str, Any]] = None):
    """Create and return an Anthropic SDK client.

    Args:
        provider_config: Optional pre-loaded configuration dictionary.

    Returns:
        Configured Anthropic client instance.
    """
    import anthropic

    if provider_config is None:
        provider_config = load_platform_config("anthropic")

    return anthropic.Anthropic(api_key=provider_config["api_key"])


def extract_text_from_completion(completion: Any) -> str:
    """Extract text content from a provider completion response.

    Args:
        completion: Raw provider response object.

    Returns:
        Extracted text string from the first choice.
    """
    if hasattr(completion, "choices") and completion.choices:
        message = completion.choices[0].message
        if hasattr(message, "content") and message.content:
            return message.content
        if hasattr(message, "tool_calls") and message.tool_calls:
            return str(message.tool_calls)
    if hasattr(completion, "content"):
        return completion.content[0].text if completion.content else ""
    return str(completion)


def normalize_platform_response(
    response: Any, provider: str = "openai"
) -> Dict[str, Any]:
    """Normalize a platform response into a consistent dictionary format.

    Args:
        response: Raw provider response object.
        provider: Provider identifier.

    Returns:
        Normalized dictionary with text, usage, and metadata.
    """
    result: Dict[str, Any] = {
        "text": extract_text_from_completion(response),
        "provider": provider,
    }

    if hasattr(response, "usage"):
        usage = response.usage
        result["usage"] = {
            "prompt_tokens": getattr(usage, "prompt_tokens", None),
            "completion_tokens": getattr(usage, "completion_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }

    if hasattr(response, "id"):
        result["response_id"] = response.id

    if hasattr(response, "model"):
        result["model"] = response.model

    return result
