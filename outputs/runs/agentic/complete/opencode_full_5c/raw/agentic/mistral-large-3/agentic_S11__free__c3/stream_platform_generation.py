from typing import Iterator, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from .model_client import get_model_client_config
from .model_models import ChatRequest, StreamResponse


def stream_platform_generation(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[StreamResponse]:
    """
    Streams output from Azure AI Inference model while preserving provider response objects.
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

    response_stream = client.complete(
        messages=messages,
        model_extras={
            "model": deployment_name,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        },
    )

    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamResponse(
                content=chunk.choices[0].delta.content,
                finish_reason=chunk.choices[0].finish_reason,
                raw_response=chunk,
            )
