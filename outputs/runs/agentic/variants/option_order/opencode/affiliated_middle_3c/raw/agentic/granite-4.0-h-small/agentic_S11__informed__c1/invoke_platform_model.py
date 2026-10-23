import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse


# Azure OpenAI service – AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are expected in the environment
def invoke_platform_model(request: ModelInvocationRequest) -> ModelInvocationResponse:
    """Invoke a model on the managed model platform using Azure OpenAI SDK.
    Returns a response enriched with platform metadata.
    """
    client = (
        ManagedModelClient()
    )  # uses AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY from env
    resp = client.invoke(
        deployment_id=request.deployment_id,
        messages=request.messages,
        temperature=request.temperature,
    )
    return resp
