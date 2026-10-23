import os
from model_client import ManagedModelClient


def invoke_model(
    project_id: str,
    deployment_id: str,
    messages: list,
    model_id: str | None = None,
) -> dict:
    """Invokes a provider‑managed model via the ManagedModelClient.

    Args:
        project_id: Project identifier supplied by the provider.
        deployment_id: Deployment / inference profile identifier.
        messages: List of prompt messages (provider‑specific format).
        model_id: Optional explicit model identifier; defaults to deployment‑scoped model.

    Returns:
        dict: Normalized response containing 'output', 'metadata', and raw provider data.
    """
    client = ManagedModelClient()
    response = client.invoke(
        project=project_id,
        deployment=deployment_id,
        messages=messages,
        model=model_id,
    )
    # Normalize provider data into a consistent dict
    normalized = {
        "output": response.get("output"),
        "metadata": response.get("metadata", {}),
        "raw": response,
    }
    return normalized
