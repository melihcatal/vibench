import os
from typing import Dict, Any
from model_client import ManagedModelClient
from model_models import GenerationRequest, GenerationResponse

def invoke_platform_model(deployment_name: str, prompt: str) -> GenerationResponse:
    """Invoke a provider‑managed model using the configured client.

    Args:
        deployment_name: Identifier of the model/deployment in the provider platform.
        prompt: Text prompt to send to the model.

    Returns:
        A GenerationResponse containing model output and provider metadata.
    """
    client = ManagedModelClient()
    req = GenerationRequest(
        deployment=deployment_name,
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
    )
    # The client uses the provider-specific SDK internally (e.g., openai, azure-ai-foundry)
    return client.invoke_generation(req)
