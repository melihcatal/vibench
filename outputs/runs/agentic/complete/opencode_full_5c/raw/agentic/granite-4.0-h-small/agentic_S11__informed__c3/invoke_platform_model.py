# invoke_platform_model.py
# SAME-SCENARIO: invocations of a provider-managed model via a project-, deployment-, or inference-profile-scoped platform client

import os
import json
from model_client import get_model_client
from model_models import normalize_request_payload, parse_response

# Example usage of the workflow step]


def invoke_model(
    model_identifier: str,
    deployment_name: str,
    inference_profile: str,
    user_input: str,
    safety_checks: bool = True,
) -> dict:
    """Invoke a managed model using a provider-specific client.

    Args:
        model_identifier: Unique model identifier within the provider.
        deployment_name: Deployment or inference profile name.
        inference_profile: Optionally select a different inference profile.
        user_input: Prompt or input data for the model.
        safety_checks: Apply post‑generation safety filtering.

    Returns:
        A dict containing the model output and platform metadata.
    """
    # Resolve a concrete provider client based on environment variables
    client = get_model_client()  # Uses env to pick AWS, Azure, Azure OpenAI, etc.
    # Build normalized payload
    payload = {
        "model": model_identifier,
        "input": user_input,
        "deployment": deployment_name,
        "profile": inference_profile,
    }
    norm_payload = normalize_request_payload(payload)
    # Call the underlying provider SDK / REST endpoint
    raw = client.invoke(norm_payload)
    # Preserve raw provider response for downstream steps
    result = {
        "output": parse_response(raw),
        "provider_response": raw,
    }
    # Optional safety check (later‑step can be inserted here)
    if safety_checks:
        result["safety"] = run_safety_filter(result["output"])  # placeholder
    return result
