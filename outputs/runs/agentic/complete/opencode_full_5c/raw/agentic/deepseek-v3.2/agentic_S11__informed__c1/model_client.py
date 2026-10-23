import os
from typing import Optional
from openai import AzureOpenAI


def get_azure_client() -> AzureOpenAI:
    """Get Azure OpenAI client with configuration from environment variables."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure OpenAI configuration missing. "
            "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables."
        )

    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version=api_version
    )


def validate_azure_config() -> bool:
    """Validate Azure OpenAI configuration."""
    required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"Missing required environment variables: {missing}")
        return False

    # Check if deployment is set
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        print("Warning: AZURE_OPENAI_DEPLOYMENT not set, using default 'gpt-4o'")

    return True


def get_available_deployments() -> list:
    """Get available Azure OpenAI deployments (simplified)."""
    # In a real implementation, this would list deployments from Azure
    # For now, return a placeholder list
    return [
        {"name": "gpt-4o", "model": "gpt-4o", "status": "succeeded"},
        {"name": "gpt-35-turbo", "model": "gpt-3.5-turbo", "status": "succeeded"},
    ]
