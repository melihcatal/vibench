import json
from typing import Dict, Any
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse, PlatformMetadata


def collect_platform_metadata(
    project_id: str,
    deployment_id: str,
    payload: Dict[str, Any],
) -> ModelInvocationResponse:
    """Invokes a model and returns the output together with provider platform metadata.

    Args:
        project_id: Provider project identifier.
        deployment_id: Provider deployment or inference profile identifier.
        payload: Request payload supplied to the provider.

    Returns:
        A ModelInvocationResponse that embeds both `output` and `metadata` fields.
    """
    client = ManagedModelClient()
    # The underlying client returns a raw response that includes usage, request IDs, and other metadata
    raw_resp = client.invoke(
        project_id=project_id,
        deployment_id=deployment_id,
        payload=payload,
    )
    # Extract a normalized output (may be text, JSON, or structured data depending on provider)
    output = raw_resp.output
    # Extract provider‑specific metadata (usage, request IDs, model handle, etc.)
    metadata: Dict[str, Any] = {
        "usage": raw_resp.usage,
        "request_id": raw_resp.request_id,
        "model_handle": raw_resp.model_handle,
    }
    # Build a structured response that the later‑step files can consume
    structured_resp = ModelInvocationResponse(
        output=output,
        metadata=metadata,
    )
    return structured_resp
