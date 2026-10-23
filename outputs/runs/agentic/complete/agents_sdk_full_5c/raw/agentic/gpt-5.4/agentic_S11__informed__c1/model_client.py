from __future__ import annotations

import os
from openai import AzureOpenAI

from model_models import GenerationRequest, ResourceSelection


DEFAULT_CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def load_default_resource() -> ResourceSelection:
    return ResourceSelection(
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", DEFAULT_CHAT_MODEL),
        model=os.getenv("AZURE_OPENAI_CHAT_MODEL", DEFAULT_CHAT_MODEL),
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION),
    )


def chat_payload(request: GenerationRequest) -> dict:
    payload = {
        "messages": request.to_messages(),
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "model": load_default_resource().deployment_name,
    }
    if request.top_p is not None:
        payload["top_p"] = request.top_p
    payload.update(request.extra)
    return payload
