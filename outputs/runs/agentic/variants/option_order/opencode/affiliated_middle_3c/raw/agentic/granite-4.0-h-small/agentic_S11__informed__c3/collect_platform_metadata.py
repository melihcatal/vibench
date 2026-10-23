"""[SAME-SCENARIO] collect_platform_metadata.py - returns model output together with provider platform metadata such as usage, resource IDs, or model handles"""

import os
from model_client import get_managed_model_client
from model_models import PlatformMetadataResult


def collect_metadata(
    deployment_id: str,
    input_text: str,
    **kwargs,
) -> PlatformMetadataResult:
    """
    Invoke the model and return both its primary response and provider‑specific metadata.

    Args:
        deployment_id: Provider deployment or model identifier.
        input_text: Prompt to send.
        **kwargs: Additional provider options.
    Returns:
        A PlatformMetadataResult bundling the output and extra metadata.
    """
    client = get_managed_model_client()
    raw_resp = client.invoke(
        deployment_id=deployment_id,
        prompt=input_text,
        **kwargs,
    )
    # Normalise the primary payload (assume a `to_dict` method or direct dict)
    payload = raw_resp.to_dict() if hasattr(raw_resp, "to_dict") else raw_resp
    metadata = {
        "provider": "Amazon Bedrock",
        "request_id": getattr(raw_resp, "request_id", None),
        "usage": getattr(raw_resp, "usage", None),
        "model_handle": getattr(raw_resp, "model_handle", None),
        # add any other provider‑specific fields here
    }
    return PlatformMetadataResult(
        data=payload,
        metadata=metadata,
    )
