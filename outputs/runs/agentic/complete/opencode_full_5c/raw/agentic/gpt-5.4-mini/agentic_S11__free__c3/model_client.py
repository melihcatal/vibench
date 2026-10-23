import os
from functools import lru_cache

from openai import OpenAI, AzureOpenAI


def get_provider_name() -> str:
    return os.getenv("MODEL_PROVIDER", "openai")


@lru_cache(maxsize=1)
def get_client():
    provider = get_provider_name().lower()
    if provider == "azure":
        return AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        )
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_deployment_name() -> str:
    return os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")


def get_locale() -> str:
    return os.getenv("TARGET_LOCALE", "es")
