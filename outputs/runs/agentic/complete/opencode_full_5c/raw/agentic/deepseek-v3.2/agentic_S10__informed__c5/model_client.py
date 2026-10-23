import os
from typing import Optional, Dict, Any
from openai import OpenAI


class ModelClient:
    """Client helper utilities for hosted LLM inference."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the model client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model identifier (e.g., "gpt-4o-mini", "gpt-4o")
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_available_models(self) -> list:
        """Get list of available models from OpenAI."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]

    def create_completion(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Create a chat completion with the configured model."""
        default_kwargs = {
            "model": self.model,
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        default_kwargs.update(kwargs)

        response = self.client.chat.completions.create(
            messages=messages, **default_kwargs
        )

        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }

    def create_streaming_completion(self, messages: list, **kwargs):
        """Create a streaming chat completion."""
        default_kwargs = {
            "model": self.model,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": True,
        }
        default_kwargs.update(kwargs)

        return self.client.chat.completions.create(messages=messages, **default_kwargs)
