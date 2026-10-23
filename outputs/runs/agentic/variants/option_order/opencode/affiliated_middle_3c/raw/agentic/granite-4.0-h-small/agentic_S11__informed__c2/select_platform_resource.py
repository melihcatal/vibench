import os
from model_client import ManagedModelClient


def select_provider(resource_type: str, config: dict) -> str:
    """Select a platform resource (model, deployment, inference profile) based on type and configuration.
    Uses the configured ManagedModelClient to resolve the identifier.
    """
    client = ManagedModelClient(config)
    if resource_type == "model":
        return client.get_model_id()
    elif resource_type == "deployment":
        return client.get_deployment_id()
    elif resource_type == "inference_profile":
        return client.get_inference_profile_id()
    raise ValueError(f"Unsupported resource_type: {resource_type}")
