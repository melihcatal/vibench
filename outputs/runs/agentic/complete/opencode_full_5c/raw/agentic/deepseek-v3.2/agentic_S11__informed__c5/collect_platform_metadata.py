import os
from typing import Dict, Any
from openai import AzureOpenAI
from model_client import get_azure_client
from model_models import ChatRequest, PlatformMetadataResponse


def collect_platform_metadata(request: ChatRequest) -> PlatformMetadataResponse:
    """
    Return model output together with Azure OpenAI platform metadata.
    """
    client = get_azure_client()

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )

        metadata = {
            "provider": "azure_openai",
            "model_id": response.model,
            "deployment_id": request.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
            "response_id": response.id,
            "created_timestamp": response.created,
            "object_type": response.object,
        }

        return PlatformMetadataResponse(
            content=response.choices[0].message.content,
            metadata=metadata,
            raw_response=response,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to collect Azure OpenAI metadata: {e}")
