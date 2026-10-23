import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_chat_model_name
from model_models import PlatformResource


def select_platform_resource(resource_hint: str | None = None) -> PlatformResource:
    client = build_azure_openai_client()
    deployment = resource_hint or get_chat_model_name()
    _ = client
    return PlatformResource(provider="azure_openai", resource_id=deployment, model_id=get_chat_model_name())
