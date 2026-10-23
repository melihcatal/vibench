import os
from model_client import ManagedModelClient


def invoke_platform_model(deployment: str, prompt: str) -> dict:
    """Invoke a model through the managed platform client, returning raw response.

    Args:
        deployment: Identifier for the deployment or inference profile.
        prompt: User prompt to send to the model.

    Returns:
        Dictionary containing the raw provider response.
    """
    client = ManagedModelClient()  # Uses environment/configuration from model_client.py
    return client.invoke(deployment, prompt)
