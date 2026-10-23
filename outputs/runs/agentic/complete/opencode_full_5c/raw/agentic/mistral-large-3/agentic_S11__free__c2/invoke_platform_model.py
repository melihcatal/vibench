from typing import Optional, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from model_client import get_model_client_config
from model_models import ChatRequest, ChatResponse


def invoke_platform_model(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ChatResponse:
    """
    Invokes Azure AI Inference model with the given request.
    """
    config = get_model_client_config()
    endpoint = endpoint or config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = api_key or config.get("AZURE_AI_INFERENCE_KEY")
    deployment_name = deployment_name or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME"
    )

    if not all([endpoint, api_key, deployment_name]):
        raise ValueError("Missing required Azure AI Inference configuration.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    messages = []
    if request.system_message:
        messages.append(SystemMessage(content=request.system_message))
    for msg in request.messages:
        messages.append(UserMessage(content=msg))

    response = client.complete(
        messages=messages,
        model_extras={
            "deployment_name": deployment_name,
            "data_sources": request.data_sources,
        }
        if request.data_sources
        else {
            "deployment_name": deployment_name,
        },
    )

    return ChatResponse(
        id=response.id,
        model=response.model,
        content=response.choices[0].message.content,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        raw_response=response,
    )
