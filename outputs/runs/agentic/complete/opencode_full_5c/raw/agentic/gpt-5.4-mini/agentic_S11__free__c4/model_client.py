import os
from typing import Optional

from openai import OpenAI, AzureOpenAI


def load_model_name(default: str = "gpt-4.1-mini") -> str:
    return os.getenv("OPENAI_MODEL", default)


def load_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_azure_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )


def select_client(provider: Optional[str] = None):
    provider = (provider or os.getenv("MODEL_PROVIDER", "openai")).lower()
    if provider == "azure":
        return load_azure_client()
    return load_openai_client()
