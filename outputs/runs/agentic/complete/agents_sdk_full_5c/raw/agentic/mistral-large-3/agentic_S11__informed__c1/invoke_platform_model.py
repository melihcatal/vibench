from typing import Optional
import os
from openai import AzureOpenAI
from model_client import get_azure_openai_config
from model_models import ModelRequest, ModelResponse


def invoke_model(request: ModelRequest) -> ModelResponse:
    """
    Invokes a managed model on Azure OpenAI Service using the configured deployment.
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

    return ModelResponse(
        output=response.choices[0].message.content,
        raw_response=response
    )