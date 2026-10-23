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
    Uses deployment_name="gpt-4o" as the concrete model identifier.
    """
    config = get_model_client_config()
    endpoint = endpoint or config.get("AZURE_AI_INFERENCE_ENDPOINT")
    api_key = api_key or config.get("AZURE_AI_INFERENCE_KEY")
    deployment_name = deployment_name or config.get(
        "AZURE_AI_INFERENCE_DEPLOYMENT", "gpt-4o"
    )

    if not endpoint or not api_key:
        raise ValueError("Azure AI Inference endpoint and API key are required.")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    messages = []
    if request.system_prompt:
        messages.append(SystemMessage(content=request.system_prompt))
    for msg in request.messages:
        messages.append(UserMessage(content=msg))

    response = client.complete(
        messages=messages,
        model_extras={
            "deployment_name": deployment_name,
        },
    )

    return ChatResponse(
        content=response.choices[0].message.content,
        raw_response=response.as_dict(),
    )
