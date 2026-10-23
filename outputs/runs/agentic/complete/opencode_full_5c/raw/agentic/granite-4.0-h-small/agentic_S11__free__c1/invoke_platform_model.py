import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse


def invoke_platform_model(
    project_id: str,
    deployment_id: str,
    payload: dict,
    prompt: str = None,
) -> ModelInvocationResponse:
    """Invokes a provider‑managed model using a platform‑scoped client.

    Args:
        project_id: Project identifier scoped to the provider.
        deployment_id: Deployment or inference profile identifier.
        payload: Raw request payload expected by the provider API.
        prompt: Optional human‑readable prompt (will be merged into payload if supplied).

    Returns:
        A ModelInvocationResponse containing model output and provider‑specific metadata.
    """
    # Merge optional prompt if payload does not already contain it
    if prompt and "prompt" not in payload:
        payload = payload.copy()
        payload["prompt"] = prompt

    client = ManagedModelClient()
    request = ModelInvocationRequest(
        project_id=project_id,
        deployment_id=deployment_id,
        payload=payload,
    )
    response = client.invoke(request)
    return response
