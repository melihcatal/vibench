# [SAME-SCENARIO] collect_platform_metadata.py
# Returns model output together with provider platform metadata such as usage, resource IDs, or model handles

from model_client import ManagedModelClient


def collect_metadata(project_id: str, deployment_id: str, payload: dict) -> dict:
    """
    Invoke the model and retrieve additional provider metadata.

    Args:
        project_id: Provider project identifier.
        deployment_id: Provider deployment/endpoint identifier.
        payload: Input payload for the model.

    Returns:
        A dict with two keys:
          - 'output': the raw model response
          - 'metadata': a dict of provider‑specific metadata (usage, model_id, etc.)
    """
    client = ManagedModelClient()
    response = client.invoke(
        project_id=project_id, deployment_id=deployment_id, payload=payload
    )
    # The client normalizes metadata into a top‑level 'metadata' key
    return {
        "output": response.get("output", {}),
        "metadata": response.get("metadata", {}),
    }
