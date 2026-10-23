import os
from typing import Any, Dict

from openai import AzureOpenAI

from model_models import PlatformRequest, first_env


def build_client() -> AzureOpenAI:
    endpoint = first_env("AZURE_OPENAI_ENDPOINT")
    api_key = first_env("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version=api_version
    )


def default_deployment() -> str:
    return first_env("AZURE_OPENAI_DEPLOYMENT", default="gpt-4o-mini")


def completion_params(request: PlatformRequest) -> Dict[str, Any]:
    return {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "stream": request.stream,
    }
