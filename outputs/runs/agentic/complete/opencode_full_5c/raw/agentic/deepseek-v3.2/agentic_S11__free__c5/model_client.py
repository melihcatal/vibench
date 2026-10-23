import os
from typing import Optional
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class ClientConfig:
    """Configuration for the OpenAI client."""

    api_key: str
    base_url: str = "https://api.openai.com/v1"
    timeout: int = 30
    max_retries: int = 3
    organization: Optional[str] = None
    project: Optional[str] = None


def load_config_from_env() -> ClientConfig:
    """Load configuration from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return ClientConfig(
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        timeout=int(os.getenv("OPENAI_TIMEOUT", "30")),
        max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")),
        organization=os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
    )


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client with configured settings."""
    config = load_config_from_env()

    client = OpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
        timeout=config.timeout,
        max_retries=config.max_retries,
        organization=config.organization,
        project=config.project,
    )

    return client


def validate_api_key(api_key: str) -> bool:
    """Validate that the OpenAI API key is properly formatted."""
    # OpenAI API keys typically start with 'sk-' and are 51 characters long
    if not api_key:
        return False
    if not api_key.startswith("sk-"):
        return False
    if len(api_key) < 20:  # Minimum reasonable length
        return False
    return True


def get_default_model() -> str:
    """Get the default model to use."""
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")


def get_available_models() -> list:
    """Return a list of available OpenAI models."""
    return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]


def create_chat_request(
    messages: list,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False,
) -> dict:
    """Create a properly formatted chat request for OpenAI API."""
    if model is None:
        model = get_default_model()

    request = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
    }

    if max_tokens:
        request["max_tokens"] = max_tokens

    return request
