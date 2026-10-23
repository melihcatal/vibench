import os
from typing import Optional

from openai import AzureOpenAI


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")
    return AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)


def get_default_deployment() -> str:
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    if deployment:
        return deployment
    return os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o-mini")


def get_resource_id() -> Optional[str]:
    return os.environ.get("AZURE_OPENAI_RESOURCE_ID")
