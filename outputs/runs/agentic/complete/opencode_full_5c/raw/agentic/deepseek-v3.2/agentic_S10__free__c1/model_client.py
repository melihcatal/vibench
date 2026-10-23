import os
from typing import Optional
from openai import OpenAI


class ModelClient:
    """Client helper utilities for hosted LLM inference."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the model client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: Base URL for the API (defaults to OpenAI's endpoint)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.base_url = base_url or "https://api.openai.com/v1"
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_available_models(self) -> list[str]:
        """
        Get list of available models.

        Returns:
            List of model identifiers
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            # Fallback to common models if listing fails
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]

    def select_model(self, task_type: str, budget_constrained: bool = False) -> str:
        """
        Select appropriate model based on task type and budget.

        Args:
            task_type: Type of task (summarization, extraction, qa, streaming, etc.)
            budget_constrained: Whether to use cheaper models

        Returns:
            Selected model identifier
        """
        if budget_constrained:
            if task_type in ["summarization", "qa"]:
                return "gpt-4o-mini"
            else:
                return "gpt-3.5-turbo"
        else:
            if task_type in ["extraction", "streaming"]:
                return "gpt-4o"
            else:
                return "gpt-4-turbo"

    def get_model_info(self, model_id: str) -> dict:
        """
        Get information about a specific model.

        Args:
            model_id: Model identifier

        Returns:
            Dictionary with model information
        """
        model_families = {
            "gpt-4o": {"family": "GPT-4", "context_length": 128000, "multimodal": True},
            "gpt-4o-mini": {
                "family": "GPT-4",
                "context_length": 128000,
                "multimodal": True,
            },
            "gpt-4-turbo": {
                "family": "GPT-4",
                "context_length": 128000,
                "multimodal": True,
            },
            "gpt-3.5-turbo": {
                "family": "GPT-3.5",
                "context_length": 16385,
                "multimodal": False,
            },
        }

        return model_families.get(
            model_id, {"family": "unknown", "context_length": 4096, "multimodal": False}
        )


def get_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
) -> ModelClient:
    """
    Get a configured model client.

    Args:
        api_key: Optional API key override
        base_url: Optional base URL override

    Returns:
        Configured ModelClient instance
    """
    return ModelClient(api_key=api_key, base_url=base_url)
