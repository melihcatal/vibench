from model_client import ManagedModelClient
from model_models import PlatformMetadata


def collect_platform_metadata(deployment: str, prompt: str) -> dict:
    """Invoke a model and attach provider‑specific usage/metadata to the output.

    Returns a dict containing both the model response and a metadata dict.

    Args:
        deployment: Platform deployment/inference profile ID.
        prompt: Prompt to send.

    Returns:
        dict with keys "response" and "metadata".
    """
    client = ManagedModelClient()
    resp = client.invoke(deployment, prompt)
    metadata = PlatformMetadata(
        provider=client.metadata["provider"],
        request_id=client.metadata.get("request_id"),
        usage=client.metadata.get("usage"),
        handle=client.metadata.get("handle"),
    )
    return {"response": resp, "metadata": metadata.to_dict()}
