# [HELPER] model_client.py

import os
from typing import Any, Dict, Optional

# Provider configuration – choose ONE concrete hosted provider.
# Here we use OpenAI's Chat Completions as the reference example.

# You can switch to another provider by changing the import and client below.
# All other files should import HostedLLMClient from this module.

# OpenAI SDK
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Azure OpenAI example (uncomment if using Azure)
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Anthropic SDK (uncomment if using Anthropic)
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class HostedLLMClient:
    """Unified client wrapper for hosted LLM inference.

    Internally delegates to a concrete SDK (OpenAI in this example).
    """
    def __init__(
        self,
        model_family: str = "gpt-4",
        provider: str = "openai",
        **provider_kwargs,  # provider-specific keyword arguments
    ):
        self.model_family = model_family
        self.provider = provider.lower()
        self.provider_kwargs = provider_kwargs
        if provider == "openai":
            import openai

            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        elif provider == "anthropic":
            import anthropic

            self.client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def complete(
        self, prompt: str, model: Optional[str] = None, **kwargs: Any
    ) -> Dict:
        """Generate a completion (non‑streaming)."""
        if self.provider == "openai":
            return self.client.chat.completions.create(
                model=model or self.model_family,
                messages=[{"role": "user", "content": prompt}],
                **self.provider_kwargs,
            )
        elif self.provider == "anthropic":
            return self.client.completions.create(
                model=model or self.model_family,
                messages=[{"role": "user", "content": prompt}],
                **self.provider_kwargs,
            )
        else:
            raise NotImplementedError(
                f"Complete not implemented for provider {self.provider}"
            )

    def stream(
        self, prompt: str, model: Optional[str] = None, **kwargs: Any
    ):
        """Generate tokens one‑by‑one (streaming)."
        if self.provider == "openai":
            return self.client.chat.completions.create(
                model=model or self.model_family,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **self.provider_kwargs,
            )
        else:
            raise NotImplementedError(
                f"Streaming not implemented for provider {self.provider}"
            )
