# [SAME-SCENARIO] collect_platform_metadata.py

from model_client import build_platform_model
from model_models import ManagedModelRequest, ManagedModelResponse


def collect_platform_metadata(
    request: ManagedModelRequest, raw_response: dict
) -> ManagedModelResponse:
    """Returns model output together with provider platform metadata.

    This helper gathers usage metrics, billing information, model handles,
    and any provider‑specific identifiers that may be useful for logging,
    usage tracking, or audit trails.

    Args:
        request (ManagedModelRequest): Original request object.
        raw_response (dict): Unmodified response dict returned by the SDK.

    Returns:
        ManagedModelResponse: Normalized response enriched with metadata.
    """
    metadata = {
        "usage": raw_response.get("usage", {}),
        "billing": raw_response.get("billing", {}),
        "model_handle": raw_response.get("model_handle"),
        "raw_response": raw_response,
    }
    return ManagedModelResponse(
        deployment_id=request.deployment_id,
        provider_payload=raw_response,
        metadata=metadata,
    )
