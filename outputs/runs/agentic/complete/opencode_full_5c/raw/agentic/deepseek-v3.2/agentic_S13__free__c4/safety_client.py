import os
from typing import Optional, Dict, Any
import openai


class SafetyClient:
    """Provide local configuration and client helper utilities for Text Content Safety."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        """
        Initialize safety client with provider configuration.

        Args:
            api_key: Provider API key (defaults to OPENAI_API_KEY env var)
            provider: Service provider ('openai', 'azure', 'anthropic', etc.)
        """
        self.provider = provider

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in OPENAI_API_KEY environment variable"
            )

        self.client = openai.OpenAI(api_key=self.api_key)

    def get_moderation_client(self):
        """Get the moderation API client."""
        return self.client.moderations

    def get_chat_client(self):
        """Get the chat completion client."""
        return self.client.chat.completions

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load safety configuration from environment variables."""
        return {
            "provider": os.environ.get("SAFETY_PROVIDER", "openai"),
            "api_key_env": "OPENAI_API_KEY",
            "default_model": "text-moderation-latest",
            "default_thresholds": {
                "hate": 0.8,
                "harassment": 0.8,
                "sexual": 0.7,
                "violence": 0.9,
                "self_harm": 0.9,
            },
            "batch_size": 32,
            "timeout": 30.0,
            "max_retries": 3,
        }

    @staticmethod
    def validate_text(text: str) -> bool:
        """Validate text input for moderation."""
        if not isinstance(text, str):
            return False
        if len(text.strip()) == 0:
            return False
        if len(text) > 10000:
            return False
        return True

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for consistent moderation."""
        return text.strip()

    def test_connection(self) -> bool:
        """Test connection to the moderation service."""
        try:
            response = self.client.moderations.create(
                model="text-moderation-latest", input="Test connection"
            )
            return response.results[0].flagged is not None
        except Exception:
            return False
