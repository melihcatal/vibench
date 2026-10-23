import os
from typing import Optional
from openai import OpenAI


class PlatformClientConfig:
    """Configuration for managed model platform client."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.organization = os.getenv("OPENAI_ORGANIZATION")
        self.project = os.getenv("OPENAI_PROJECT")
        self.timeout = int(os.getenv("OPENAI_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True


def get_platform_client() -> OpenAI:
    """Get configured OpenAI client for the platform."""
    config = PlatformClientConfig()
    config.validate()

    client_kwargs = {
        "api_key": config.api_key,
        "base_url": config.base_url,
        "timeout": config.timeout,
        "max_retries": config.max_retries,
    }

    if config.organization:
        client_kwargs["organization"] = config.organization

    if config.project:
        client_kwargs["project"] = config.project

    return OpenAI(**client_kwargs)


def get_default_model() -> str:
    """Get default model for the platform."""
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")


def get_available_models() -> list:
    """Get list of available models from the platform."""
    return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
