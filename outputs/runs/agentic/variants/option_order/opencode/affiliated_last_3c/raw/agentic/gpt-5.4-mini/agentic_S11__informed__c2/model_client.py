import os
from typing import Any, Optional

from openai import AzureOpenAI


def get_endpoint() -> Optional[str]:
    return os.getenv("AZURE_OPENAI_ENDPOINT")


def get_api_key() -> Optional[str]:
    return os.getenv("AZURE_OPENAI_API_KEY")


def get_api_version() -> str:
    return os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")


def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=get_endpoint(),
        api_key=get_api_key(),
        api_version=get_api_version(),
    )


def resolve_model_id(default: str = "gpt-4o-mini") -> str:
    return os.getenv("AZURE_OPENAI_DEPLOYMENT", default)


def resolve_resource_id(deployment_id: Optional[str] = None) -> str:
    return deployment_id or resolve_model_id()


def stream_to_text(stream: Any) -> str:
    chunks = []
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            chunks.append(delta)
    return "".join(chunks)
