import os
from typing import Optional
from openai import OpenAI
from anthropic import Anthropic


class LLMClient:
    """Client helper for hosted LLM inference."""

    def __init__(self, provider: str = "openai"):
        """
        Initialize LLM client for a specific provider.

        Args:
            provider: The LLM provider to use ("openai" or "anthropic")
        """
        self.provider = provider
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            return OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            return Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_available_models(self) -> list:
        """Get list of available models for the current provider."""
        if self.provider == "openai":
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
        elif self.provider == "anthropic":
            return [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240307",
            ]
        return []

    def get_default_model(self) -> str:
        """Get the default model for the current provider."""
        if self.provider == "openai":
            return "gpt-4o-mini"
        elif self.provider == "anthropic":
            return "claude-3-5-sonnet-20241022"
        return ""


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """
    Get an LLM client instance.

    Args:
        provider: Optional provider name, defaults to OPENAI

    Returns:
        LLMClient instance
    """
    provider_to_use = provider or os.getenv("LLM_PROVIDER", "openai")
    return LLMClient(provider=provider_to_use)


def get_model_family(model_name: str) -> str:
    """
    Determine the model family from a model name.

    Args:
        model_name: The full model name

    Returns:
        Model family string
    """
    model_name_lower = model_name.lower()

    if "gpt-4" in model_name_lower:
        return "gpt-4"
    elif "gpt-3.5" in model_name_lower:
        return "gpt-3.5"
    elif "claude-3" in model_name_lower:
        return "claude-3"
    elif "claude-2" in model_name_lower:
        return "claude-2"
    else:
        return "unknown"
