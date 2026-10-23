from __future__ import annotations

import os

from openai import AzureOpenAI


DEFAULT_API_VERSION = "2024-10-21"
DEFAULT_CHAT_DEPLOYMENT = "gpt-4o-mini"


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version=api_version
    )


def get_chat_deployment() -> str:
    return os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", DEFAULT_CHAT_DEPLOYMENT)


def resolve_chat_resource() -> dict[str, str]:
    deployment = get_chat_deployment()
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    return {
        "provider": "azure_openai",
        "deployment": deployment,
        "resource_id": f"{endpoint.rstrip('/')}/openai/deployments/{deployment}",
    }
