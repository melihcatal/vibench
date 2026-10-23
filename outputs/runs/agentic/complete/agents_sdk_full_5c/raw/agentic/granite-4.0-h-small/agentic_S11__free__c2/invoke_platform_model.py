# [SAME-SCENARIO] invoke_platform_model.py
import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_platform_model(deployment_id: str, prompt: str) -> ModelInvocationResponse:
    """Invoke a provider‑managed model using the platform client.
    
    Uses the ManagedModelClient configured via environment variables for a specific project/deployment.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(
        deployment_id=deployment_id,
        prompt=prompt,
        # optional: temperature, max_tokens, etc.
    )
    response = client.invoke(request)
    # response contains both model output and provider metadata
    return response
