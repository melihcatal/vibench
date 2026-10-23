"""[SAME-SCENARIO] select_platform_resource.py - resolves a provider-specific model, deployment, or inference resource before invocation"""

import os
from model_client import load_resource_configuration


def select_resource(resource_name: str, resource_type: str = "model") -> str:
    """
    Resolve the concrete provider identifier for a given resource name.
    The configuration is expected to be defined in a local YAML/JSON file or
    environment variables, read by load_resource_configuration().

    Args:
        resource_name: Human‑readable name used by the caller (e.g., "gpt-4o-mini").
        resource_type: Type of resource: "model" | "deployment" | "inference_profile"
    Returns:
        The canonical identifier required by the underlying client (e.g., arn, guid, or model_id).
    """
    cfg = load_resource_configuration()  # loads from config file or env
    return cfg.get(resource_type, {}).get(resource_name)
