import os
from typing import Optional
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Get OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return OpenAI(api_key=api_key)


def get_model_config(model_family: str = "gpt") -> dict:
    """Get configuration for different model families."""
    configs = {
        "gpt": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.7,
        },
        "gpt-4": {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.7,
        },
        "gpt-4-turbo": {
            "model": "gpt-4-turbo-preview",
            "max_tokens": 4000,
            "temperature": 0.7,
        },
    }

    return configs.get(model_family, configs["gpt"])


def normalize_response(response_text: str) -> str:
    """Normalize model response text."""
    return response_text.strip()


def build_prompt(system_message: str, user_message: str) -> list:
    """Build chat prompt messages."""
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
