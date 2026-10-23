# select_platform_resource.py
# SAME-SCENARIO: resolves model, deployment, or inference resource IDs for the selected provider

import os
import json
from model_models import parse_resource_catalog

# Example helper functions to query a provider's resource catalog


def list_models(provider: str) -> list:
    """Return a list of models available for the given provider."""
    client = get_provider_client(
        provider
    )  # Assume a helper that returns a low‑level SDK or REST client
    return client.list_models()


def list_deployments(provider: str) -> list:
    """Return a list of deployments/inference profiles for the given provider."""
    client = get_provider_client(provider)
    return client.list_deployments()


def select_resource(
    provider: str,
    model_name: str = None,
    deployment_name: str = None,
    profile_name: str = None,
) -> dict:
    """Select concrete resource IDs based on names or environment hints.

    Returns a dict with keys 'model', 'deployment', 'profile'.
    """
    # If environment variables are set, prefer them (e.g., AWS_MODEL_ID)
    if provider == "aws":
        model_id = os.getenv("AWS_MODEL_ID")
        deployment_id = os.getenv("AWS_DEPLOYMENT_ID")
        profile_id = os.getenv("AWS_INFERENCE_PROFILE")
        return {
            "model": model_id,
            "deployment": deployment_id,
            "profile": profile_id,
        }
    # Otherwise fall back to user‑provided names and do a lookup
    models = list_models(provider)
    deployments = list_deployments(provider)
    # Simple name‑match (real implementation would use search/filter APIs)
    model_id = next((m["id"] for m in models if model_name in m["name"]), None)
    deployment_id = next(
        (d["id"] for d in deployments if deployment_name in d["name"]),
        None,
    )
    profile_id = profile_name  # assume direct mapping for simplicity
    return {
        "model": model_id,
        "deployment": deployment_id,
        "profile": profile_id,
    }
