import os
from openai import AzureOpenAI


def build_azure_openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )


def get_default_platform_model_name() -> str:
    return os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def resolve_platform_resource(preferred: str | None = None) -> str:
    return preferred or get_default_platform_model_name()
