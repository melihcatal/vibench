# [SAME-SCENARIO] select_platform_resource.py
# Resolves a provider-specific model, deployment, or inference resource before invocation

import os
from model_models import ProviderResource


def resolve_resource(resource_type: str, name: str) -> ProviderResource:
    """
    Resolve a concrete provider resource identifier based on the requested type.

    Args:
        resource_type: One of 'model', 'deployment', or 'inference_profile'.
        name: Human‑readable identifier passed by the caller.

    Returns:
        A ProviderResource with the fully‑qualified identifier ready for invocation.
    """
    # Example: load provider‑specific mapping from environment variables
    if resource_type == "model":
        # Azure OpenAI example: AZURE_OPENAI_MODEL_NAME
        model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
        if not model_name:
            raise ValueError("AZURE_OPENAI_MODEL_NAME not set")
        return ProviderResource(model=model_name)
    elif resource_type == "deployment":
        # Example: AZURE_OPENAI_DEPLOYMENT_NAME
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME not set")
        return ProviderResource(deployment=deployment)
    elif resource_type == "inference_profile":
        # Example: AZURE_OPENAI_INFERENCE_PROFILE
        profile = os.getenv("AZURE_OPENAI_INFERENCE_PROFILE")
        if not profile:
            raise ValueError("AZURE_OPENAI_INFERENCE_PROFILE not set")
        return ProviderResource(inference_profile=profile)
    else:
        raise ValueError(f"Unsupported resource_type: {resource_type}")
