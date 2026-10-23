from typing import Optional, Dict, Any
import os
from openai import AzureOpenAI
from .model_client import get_azure_openai_client
from .model_models import ModelRequest, ModelResponse


def invoke_platform_model(
    request: ModelRequest,
    deployment_name: Optional[str] = None,
    model: Optional[str] = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> ModelResponse:
    """
    Invokes an Azure OpenAI managed model using the Azure OpenAI Service SDK.
    """
    client = get_azure_openai_client()

    if not deployment_name:
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not deployment_name:
            raise ValueError(
                "Deployment name must be provided or set in AZURE_OPENAI_DEPLOYMENT_NAME."
            )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=request.messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=request.top_p if request.top_p else 1.0,
        frequency_penalty=request.frequency_penalty
        if request.frequency_penalty
        else 0.0,
        presence_penalty=request.presence_penalty if request.presence_penalty else 0.0,
    )

    return ModelResponse(
        id=response.id,
        object=response.object,
        created=response.created,
        model=response.model,
        choices=response.choices,
        usage=response.usage,
    )
