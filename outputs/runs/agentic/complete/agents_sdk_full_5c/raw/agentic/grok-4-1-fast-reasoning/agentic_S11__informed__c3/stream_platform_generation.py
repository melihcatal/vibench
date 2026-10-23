import os
from openai import OpenAI
from model_client import get_platform_config
from model_models import PlatformInvokeRequest, ChatMessage
from typing import Iterator

def stream_platform_generation(request: PlatformInvokeRequest) -> Iterator:
    """
    Stream from Azure OpenAI preserving response objects.
    """
    config = get_platform_config()
    client = OpenAI(
        azure_endpoint=config["azure_endpoint"],
        api_key=config["azure_api_key"],
        api_version=config["api_version"]
    )
    deployment = request.model or "gpt-4o"
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=True
    )
    for chunk in stream:
        yield chunk