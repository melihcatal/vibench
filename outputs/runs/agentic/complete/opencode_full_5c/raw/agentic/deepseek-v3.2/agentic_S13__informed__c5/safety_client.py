import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class SafetyConfig:
    endpoint: str
    key: str
    api_version: str = "2023-10-01"


def load_safety_config() -> SafetyConfig:
    """
    Load Azure AI Content Safety configuration from environment variables.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    return SafetyConfig(
        endpoint=endpoint,
        key=key,
        api_version=os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", "2023-10-01"),
    )


def get_content_safety_client():
    """
    Create and return an Azure AI Content Safety client.
    """
    config = load_safety_config()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    credential = AzureKeyCredential(config.key)
    client = ContentSafetyClient(endpoint=config.endpoint, credential=credential)

    return client


def validate_text_length(text: str, max_length: int = 1000) -> bool:
    """
    Validate text length for content safety API limits.
    """
    return len(text) <= max_length


def normalize_text(text: str) -> str:
    """
    Normalize text for content safety analysis.
    """
    return text.strip()
