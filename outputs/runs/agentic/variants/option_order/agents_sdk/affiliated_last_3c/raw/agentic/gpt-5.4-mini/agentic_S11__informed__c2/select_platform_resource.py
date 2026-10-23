from __future__ import annotations

from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient

from model_client import load_config


AZURE_MODEL_CATALOG = {
    "chat": "gpt-4o-mini",
    "reasoning": "gpt-4.1",
}


def resolve_platform_resource(resource_type: str = "chat") -> str:
    return AZURE_MODEL_CATALOG.get(resource_type, AZURE_MODEL_CATALOG["chat"])


def build_platform_client() -> ChatCompletionsClient:
    cfg = load_config()
    return ChatCompletionsClient(endpoint=cfg.endpoint, credential=AzureKeyCredential(cfg.api_key))


def select_resource_and_client(resource_type: str = "chat") -> tuple[str, ChatCompletionsClient]:
    return resolve_platform_resource(resource_type), build_platform_client()
