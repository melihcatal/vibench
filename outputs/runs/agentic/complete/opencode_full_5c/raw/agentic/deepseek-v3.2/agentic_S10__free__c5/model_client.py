import os
from typing import Optional
from openai import OpenAI


class ModelClient:
    """Client helper utilities for Hosted LLM Inference and Model-Family Selection."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_model_list(self) -> list:
        """Get available models from the provider."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise Exception(f"Failed to fetch model list: {str(e)}")

    def select_model(self, task_type: str) -> str:
        """Select appropriate model based on task type."""
        model_map = {
            "summarization": "gpt-4o-mini",
            "extraction": "gpt-4o",
            "qa": "gpt-4-turbo",
            "streaming": "gpt-4o",
            "general": "gpt-4o",
        }

        return model_map.get(task_type, "gpt-4o")

    def create_completion(self, prompt: str, model: Optional[str] = None, **kwargs):
        """Create a completion with the given parameters."""
        model = model or self.select_model("general")

        return self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], **kwargs
        )


def get_client() -> ModelClient:
    """Get a configured model client instance."""
    return ModelClient()
