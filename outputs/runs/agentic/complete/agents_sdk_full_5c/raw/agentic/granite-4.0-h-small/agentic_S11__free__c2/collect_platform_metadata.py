# [SAME-SCENARIO] collect_platform_metadata.py
import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def collect_platform_metadata(prompt: str, deployment_id: str) -> ModelInvocationResponse:
    """Invoke a model and return both the textual output and rich provider metadata.

    The returned response includes fields such as usage information, token usage, resource IDs, and any
    diagnostic data the provider returns.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(
        deployment_id=deployment_id,
        prompt=prompt,
    )
    return client.invoke(request)
