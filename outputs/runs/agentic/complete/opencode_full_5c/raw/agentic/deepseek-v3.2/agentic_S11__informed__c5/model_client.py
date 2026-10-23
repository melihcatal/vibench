import os
from typing import Optional
from openai import AzureOpenAI
from dataclasses import dataclass


@dataclass
class AzureConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-02-01"


def load_azure_config() -> AzureConfig:
    """
    Load Azure OpenAI configuration from environment variables.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")

    return AzureConfig(endpoint=endpoint, api_key=api_key, api_version=api_version)


def get_azure_client() -> AzureOpenAI:
    """
    Create and return an Azure OpenAI client.
    """
    config = load_azure_config()

    return AzureOpenAI(
        azure_endpoint=config.endpoint,
        api_key=config.api_key,
        api_version=config.api_version,
    )


def validate_azure_credentials() -> bool:
    """
    Validate Azure OpenAI credentials by making a simple API call.
    """
    try:
        client = get_azure_client()
        client.models.list()
        return True
    except Exception:
        return False
