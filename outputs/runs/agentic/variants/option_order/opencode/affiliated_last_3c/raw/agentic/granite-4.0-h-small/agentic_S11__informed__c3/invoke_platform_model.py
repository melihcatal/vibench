import os
import json
from model_client import ManagedModelClient


def invoke_platform_model(resource_id: str, payload: dict) -> dict:
    """Invoke a provider‑managed generative model using a project/deployment/inference profile.

    Args:
        resource_id: Identifier of the model/deployment/inference profile (e.g., "bedrock-llama2", "vertex-llama3" etc.).
        payload: Input data expected by the model (text, chat messages, etc.).

    Returns:
        A dict containing the provider response plus a "metadata" field with provider‑specific IDs.
    """
    client = ManagedModelClient()
    response = client.invoke(resource_id, payload)
    # Attach provider‑specific metadata returned with the response
    result = {
        **response,
        "metadata": {
            # Example: resource_id, provider_region, request_id, usage_estimate
            "resource_id": resource_id,
            "provider_region": client.region,
            "request_id": response.get("request_id"),
            "usage_estimate": response.get("usage_estimate"),
        },
    }
    return result
