import json
from model_client import ManagedModelClient
from model_models import Model


def collect_metadata(
    model: Model,
    messages: list,
) -> dict:
    """Return model output together with provider-specific platform metadata.

    Args:
        model: Model instance to invoke.
        messages: Prompt messages (provider‑specific shape).

    Returns:
        dict: Normalized dict with keys `output`, `metadata`, `raw`.
    """
    client = ManagedModelClient()
    response = client.invoke(
        project=model.provider,
        deployment=model.deployment or model.model_id,
        messages=messages,
        model=model.model_id,
    )
    # The client already normalizes, but we ensure metadata includes usage and IDs
    return {
        "output": response.get("output"),
        "metadata": {
            "usage": response.get("metadata", {}).get("usage"),
            "model_id": model.model_id,
            "deployment": model.deployment or model.model_id,
            "provider": client.PROVIDER,
        },
        "raw": response,
    }
