from typing import Dict, Any, Tuple
from openai import AzureOpenAI
from .model_client import get_azure_openai_client
from .model_models import ModelRequest, ModelResponseWithMetadata


def collect_platform_metadata(
    request: ModelRequest, deployment_name: str, model: str = "gpt-4o"
) -> ModelResponseWithMetadata:
    """
    Returns Azure OpenAI model output together with provider platform metadata
    such as usage, resource IDs, or model handles.
    """
    client = get_azure_openai_client()

    response = client.chat.completions.create(
        model=deployment_name,
        messages=request.messages,
        temperature=request.temperature if request.temperature else 0.7,
        max_tokens=request.max_tokens if request.max_tokens else 1000,
        top_p=request.top_p if request.top_p else 1.0,
        frequency_penalty=request.frequency_penalty
        if request.frequency_penalty
        else 0.0,
        presence_penalty=request.presence_penalty if request.presence_penalty else 0.0,
    )

    metadata = {
        "provider": "azure_openai",
        "deployment_id": deployment_name,
        "model_id": model,
        "api_version": client.api_version,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }

    return ModelResponseWithMetadata(
        id=response.id,
        object=response.object,
        created=response.created,
        model=response.model,
        choices=response.choices,
        usage=response.usage,
        metadata=metadata,
    )
