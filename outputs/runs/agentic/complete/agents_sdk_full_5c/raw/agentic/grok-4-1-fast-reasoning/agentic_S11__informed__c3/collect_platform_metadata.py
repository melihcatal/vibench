import os
from openai import OpenAI
from model_client import get_platform_config
from model_models import PlatformInvokeRequest, ChatMessage

def collect_platform_metadata(request: PlatformInvokeRequest) -> dict:
    """
    Collect Azure OpenAI output with metadata.
    """
    config = get_platform_config()
    client = OpenAI(
        azure_endpoint=config["azure_endpoint"],
        api_key=config["azure_api_key"],
        api_version=config["api_version"]
    )
    deployment = request.model or "gpt-4o"
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=False
    )
    choice = response.choices[0]
    metadata = {
        "content": choice.message.content,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        } if response.usage else None,
        "model": deployment,
        "id": response.id,
        "finish_reason": choice.finish_reason,
        "system_fingerprint": getattr(response, "system_fingerprint", None)
    }
    return metadata