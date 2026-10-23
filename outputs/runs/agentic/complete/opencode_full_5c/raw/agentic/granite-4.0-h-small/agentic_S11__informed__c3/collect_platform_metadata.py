# collect_platform_metadata.py
# SAME-SCENARIO: returns model output together with provider platform metadata

import os
import json
from model_client import get_model_client
from model_models import parse_response


def collect_metadata(
    model_identifier: str,
    deployment_name: str,
    inference_profile: str = None,
    user_input: str = "",
    return_raw: bool = False,
) -> dict:
    """Invoke model and attach platform‑specific metadata to the result.

    Args:
        model_identifier: Model ID used for the request.
        deployment_name: Deployment or inference profile.
        inference_profile: Optional alternate profile.
        user_input: Prompt or input payload.
        return_raw: If True, include the untouched provider response.

    Returns:
        A dict with keys 'output', 'metadata', and optionally 'raw'.
    """
    client = get_model_client()  # Provider client from env
    payload = {
        "model": model_identifier,
        "deployment": deployment_name,
        "profile": inference_profile,
        "input": user_input,
    }
    norm_payload = normalize_request_payload(payload)
    raw = client.invoke(norm_payload)
    output = parse_response(raw)
    # Extract generic metadata that is common across providers
    metadata = {
        "model_id": model_identifier,
        "deployment_id": raw.get("deploymentId"),
        "provider": infer_provider_name(),  # Helper that detects provider from env/client
        "usage": raw.get("usage"),  # e.g., token counts, request ID, etc.
    }
    if return_raw:
        metadata["raw"] = raw
    return {
        "output": output,
        "metadata": metadata,
    }
