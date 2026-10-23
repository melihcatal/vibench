import os
from typing import Optional, Dict, Any
from openai import OpenAI


class ModelClient:
    """Local configuration and client helper utilities for Managed Model Platform Workflow."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be provided or set in environment")

        self.base_url = base_url
        self._client = None

    @property
    def client(self) -> OpenAI:
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            kwargs = {"api_key": self.api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self._client = OpenAI(**kwargs)
        return self._client

    def get_available_models(self) -> list:
        """Get list of available models from OpenAI."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]

    def validate_model(self, model_name: str) -> bool:
        """Validate that a model is available."""
        available_models = self.get_available_models()
        return model_name in available_models

    def create_chat_request(
        self, messages: list, model: str = "gpt-4o", **kwargs
    ) -> Dict[str, Any]:
        """Create a standardized chat request."""
        default_params = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        default_params.update(kwargs)
        return default_params

    def parse_response(self, response) -> Dict[str, Any]:
        """Parse OpenAI response into standardized format."""
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }
