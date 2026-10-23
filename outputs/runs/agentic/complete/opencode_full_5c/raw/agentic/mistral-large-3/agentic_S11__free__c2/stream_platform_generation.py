from typing import Iterator, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from model_client import get_model_client_config
from model_models import ChatRequest, StreamChunk


def stream_platform_generation(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[StreamChunk]:
    """
    Streams output from Azure AI Inference model.
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

    response_stream = client.complete_stream(
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

    for chunk in response_stream:
        yield StreamChunk(
            id=chunk.id,
            model=chunk.model,
            content=chunk.choices[0].delta.content if chunk.choices else "",
            raw_chunk=chunk,
        )
