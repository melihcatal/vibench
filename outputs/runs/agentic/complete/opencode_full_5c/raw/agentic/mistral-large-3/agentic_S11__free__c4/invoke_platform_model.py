import os
from typing import Optional, Dict, Any

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

from .model_client import get_model_client_config
from .model_models import ChatRequest, ChatResponse


def invoke_platform_model(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ChatResponse:
    """
    Invokes the Azure AI Inference model using the provided deployment or endpoint.
    """
    config = get_model_client_config()

    endpoint = endpoint or config.get("AZURE_AI_ENDPOINT")
    api_key = api_key or config.get("AZURE_AI_API_KEY")
    deployment_name = deployment_name or config.get("AZURE_AI_DEPLOYMENT_NAME")

    if not endpoint or not api_key:
        raise ValueError("Azure AI endpoint and API key must be provided.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    messages = [
        SystemMessage(content=msg.content)
        if msg.role == "system"
        else UserMessage(content=msg.content)
        for msg in request.messages
    ]

    response = client.complete(
        messages=messages,
        model=deployment_name,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return ChatResponse(
        content=response.choices[0].message.content,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        model=deployment_name or "unknown",
    )
