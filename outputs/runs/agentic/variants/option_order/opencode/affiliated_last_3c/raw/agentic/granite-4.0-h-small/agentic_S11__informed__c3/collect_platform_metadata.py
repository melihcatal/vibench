import os
import json
from model_client import ManagedModelClient


def collect_platform_metadata(resource_id: str, payload: dict) -> dict:
    """Return model output together with provider platform metadata such as usage, resource IDs, or model handles.

    Args:
        resource_id: Concrete model/deployment identifier.
        payload: Input data for the model.

    Returns:
        A dict containing both the model's raw response and a "metadata" sub‑dict with provider‑specific details.
    """
    client = ManagedModelClient()
    response = client.invoke(resource_id, payload)
    # Provider may return usage bytes, estimated cost, request IDs, etc.
    return {
        **response,
        "metadata": {
            "provider": client.service,
            "region": client.region,
            "request_id": response.get("request_id"),
            "estimated_cost_usd": response.get("usage_estimate"),
            "resource_handle": response.get("model_handle"),
        },
    }
