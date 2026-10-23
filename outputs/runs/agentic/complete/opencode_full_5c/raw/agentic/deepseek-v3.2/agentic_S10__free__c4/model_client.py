import os
from typing import Optional
from openai import OpenAI


class ModelConfig:
    """Configuration for hosted LLM inference."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True


_config: Optional[ModelConfig] = None
_client: Optional[OpenAI] = None


def get_config() -> ModelConfig:
    """Get or create configuration instance."""
    global _config
    if _config is None:
        _config = ModelConfig()
        _config.validate()
    return _config


def get_client() -> OpenAI:
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        config = get_config()
        _client = OpenAI(
            api_key=config.api_key, base_url=config.base_url, timeout=config.timeout
        )
    return _client


def reset_client():
    """Reset client for testing or reconfiguration."""
    global _client
    _client = None
