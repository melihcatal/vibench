import os
from typing import Dict, Any
from openai import AzureOpenAI
from model_client import get_azure_openai_config
from model_models import ModelRequest, ModelResponseWithMetadata


def collect_model_metadata(request: ModelRequest) -> ModelResponseWithMetadata:
    """
    Invokes Azure OpenAI Service and returns model output with platform metadata.
    """
    config = get_azure_openai_config()
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=config["api_version"],
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    deployment_name = config["deployment_name"]
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    metadata = {
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        },
        "system_fingerprint": response.system_fingerprint,
        "deployment_name": deployment_name
    }

    return ModelResponseWithMetadata(
        output=response.choices[0].message.content,
        metadata=metadata,
        raw_response=response
    )