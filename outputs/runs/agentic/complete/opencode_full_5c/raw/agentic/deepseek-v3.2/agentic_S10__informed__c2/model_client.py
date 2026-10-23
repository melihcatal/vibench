import os
from typing import Optional, Dict, Any
from openai import OpenAI


class ModelClient:
    """Client helper utilities for Hosted LLM Inference and Model-Family Selection."""

    def __init__(self, provider: str = "openai"):
        """
        Initialize model client for the specified provider.

        Args:
            provider: Service provider ('openai', 'anthropic', 'mistral', etc.)
        """
        self.provider = provider
        self.client = None

        if provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            # Placeholder for Anthropic client initialization
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            # In a real implementation: import anthropic; self.client = anthropic.Anthropic(api_key=api_key)
        elif provider == "mistral":
            # Placeholder for Mistral client initialization
            api_key = os.environ.get("MISTRAL_API_KEY")
            if not api_key:
                raise ValueError("MISTRAL_API_KEY environment variable is required")
            # In a real implementation: from mistralai import Mistral; self.client = Mistral(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_default_model(self) -> str:
        """Get default model for the current provider."""
        defaults = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-haiku-20240307",
            "mistral": "mistral-small-latest",
        }
        return defaults.get(self.provider, "gpt-3.5-turbo")

    def create_completion(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> str:
        """Create a completion using the configured provider."""
        if self.provider == "openai":
            model = model or self.get_default_model()
            response = self.client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}], **kwargs
            )
            return response.choices[0].message.content
        else:
            raise NotImplementedError(
                f"Provider {self.provider} not implemented in helper"
            )

    @staticmethod
    def get_available_providers() -> list:
        """Get list of available LLM providers."""
        return ["openai", "anthropic", "mistral", "gemini", "bedrock"]

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {
            "openai_api_key": os.environ.get("OPENAI_API_KEY"),
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
            "mistral_api_key": os.environ.get("MISTRAL_API_KEY"),
            "default_provider": os.environ.get("DEFAULT_LLM_PROVIDER", "openai"),
            "default_model": os.environ.get("DEFAULT_LLM_MODEL", "gpt-3.5-turbo"),
        }
        return config
