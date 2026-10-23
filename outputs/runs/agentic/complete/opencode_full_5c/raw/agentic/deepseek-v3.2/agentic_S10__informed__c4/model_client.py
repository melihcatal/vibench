import os
from typing import Optional, Dict, Any
from anthropic import Anthropic


class ModelClient:
    """Client helper utilities for hosted LLM inference."""

    def __init__(
        self, provider: str = "anthropic", model: str = "claude-3-5-sonnet-20241022"
    ):
        self.provider = provider
        self.model = model
        self.client = None

        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def create_completion(
        self, messages: list, max_tokens: int = 1000, **kwargs
    ) -> str:
        """Create a completion using the configured provider."""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model, max_tokens=max_tokens, messages=messages, **kwargs
            )
            return response.content[0].text
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def stream_completion(self, messages: list, max_tokens: int = 1000, **kwargs):
        """Stream completion from the configured provider."""
        if self.provider == "anthropic":
            with self.client.messages.stream(
                model=self.model, max_tokens=max_tokens, messages=messages, **kwargs
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        yield event.delta.text
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    @staticmethod
    def get_available_models(provider: str = "anthropic") -> list:
        """Get available models for the provider."""
        if provider == "anthropic":
            return [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
            ]
        else:
            raise ValueError(f"Unsupported provider: {provider}")
