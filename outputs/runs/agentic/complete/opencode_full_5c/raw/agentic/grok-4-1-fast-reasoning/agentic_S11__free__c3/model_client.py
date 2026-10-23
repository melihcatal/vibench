import os
from typing import Any

from azure.openai import AzureOpenAI


def get_azure_openai_client(deployment: str) -> AzureOpenAI:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2024-02-15-preview",
        azure_deployment=deployment,
    )
