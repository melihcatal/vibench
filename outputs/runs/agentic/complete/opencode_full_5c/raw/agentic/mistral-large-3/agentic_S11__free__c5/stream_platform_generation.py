from typing import Iterator, Dict, Any
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from model_client import get_model_client_config
from model_models import ChatRequest, StreamResponseChunk


def stream_platform_generation(
    request: ChatRequest,
    deployment_name: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[StreamResponseChunk]:
    """
    Streams output from Azure AI Inference model.
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

    response_stream = client.complete_stream(
        messages=messages,
        model_extras={
            "deployment_name": deployment_name,
        },
    )

    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamResponseChunk(
                content=chunk.choices[0].delta.content,
                raw_response=chunk.as_dict(),
            )
