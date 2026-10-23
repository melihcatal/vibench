import os
from typing import Any, Dict

from openai import AzureOpenAI


def get_endpoint() -> str:
    return os.environ["AZURE_OPENAI_ENDPOINT"]


def get_api_key() -> str:
    return os.environ["AZURE_OPENAI_API_KEY"]


def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=get_api_key(),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        azure_endpoint=get_endpoint(),
    )


def resource_metadata(model: str) -> Dict[str, Any]:
    return {"provider": "azure-openai", "model": model}
