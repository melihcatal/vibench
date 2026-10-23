from typing import Optional, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from .model_client import get_model_client_config
from .model_models import ChatRequest, ChatResponse


def invoke_platform_model(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ChatResponse:
    """
    Invokes the Azure AI Inference model using the provided request.
    """
    config = get_model_client_config()
    endpoint = endpoint or config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = api_key or config.get("AZURE_AI_INFERENCE_KEY")
    deployment_name = deployment_name or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME"
    )

    if not all([endpoint, api_key, deployment_name]):
        raise ValueError("Missing required configuration for Azure AI Inference.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    messages = [
        SystemMessage(content=request.system_message)
        if request.system_message
        else None,
        UserMessage(content=request.user_message),
    ]
    messages = [msg for msg in messages if msg is not None]

    response = client.complete(
        messages=messages,
        model_extras={
            "model": deployment_name,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        },
    )

    return ChatResponse(
        content=response.choices[0].message.content,
        finish_reason=response.choices[0].finish_reason,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )
