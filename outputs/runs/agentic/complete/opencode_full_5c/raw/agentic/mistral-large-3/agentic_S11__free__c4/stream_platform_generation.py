import os
from typing import Iterator, Dict, Any

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

from .model_client import get_model_client_config
from .model_models import ChatRequest, StreamResponseChunk


def stream_platform_generation(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[StreamResponseChunk]:
    """
    Streams output from Azure AI Inference model while preserving provider response objects.
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

    response_stream = client.complete_stream(
        messages=messages,
        model=deployment_name,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    for chunk in response_stream:
        if chunk.choices:
            yield StreamResponseChunk(
                content=chunk.choices[0].delta.content
                if chunk.choices[0].delta
                else "",
                chunk_metadata={
                    "id": chunk.id,
                    "created": chunk.created,
                    "model": chunk.model,
                },
            )
