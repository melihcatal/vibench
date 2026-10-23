import os
from typing import Optional
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Get configured OpenAI client with API key from environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    return OpenAI(api_key=api_key)


def get_openai_base_url() -> str:
    """
    Get OpenAI API base URL, supporting custom endpoints.
    """
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return base_url


def validate_model_id(model_id: str) -> bool:
    """
    Validate that the model ID is a known OpenAI model.
    """
    known_models = {
        "gpt-4o",
        "gpt-4o-2024-08-06",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-instruct",
    }
    return model_id in known_models


def get_default_model() -> str:
    """
    Get default OpenAI model based on environment or configuration.
    """
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")
