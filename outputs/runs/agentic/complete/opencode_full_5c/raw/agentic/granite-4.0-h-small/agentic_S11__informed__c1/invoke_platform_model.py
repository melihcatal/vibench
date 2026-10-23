# [SAME-SCENARIO] invoke_platform_model.py
# Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client

from model_client import ManagedModelClient


def invoke_model(project_id: str, deployment_id: str, payload: dict) -> dict:
    """Invoke the selected provider model using the configured client.

    Args:
        project_id: Provider project identifier.
        deployment_id: Provider deployment/endpoint identifier.
        payload: Model input payload.

    Returns:
        A dict containing the raw provider response.
    """
    client = ManagedModelClient()
    return client.invoke(
        project_id=project_id, deployment_id=deployment_id, payload=payload
    )
