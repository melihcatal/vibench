import os
from openai import OpenAI
from model_client import get_platform_config
from model_models import PlatformInvokeRequest, ChatMessage

def invoke_platform_model(request: PlatformInvokeRequest) -> str:
    """
    Invoke Azure OpenAI model via project-scoped client.
    """
    config = get_platform_config()
    client = OpenAI(
        azure_endpoint=config["azure_endpoint"],
        api_key=config["azure_api_key"],
        api_version=config["api_version"]
    )
    deployment = request.model or config["deployment"]
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=False
    )
    return response.choices[0].message.content