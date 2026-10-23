import os
from huggingface_hub import HfApi

# Resolve a model identifier or fallback to a deployment endpoint using Hugging Face API
# This helper works for Hugging Face Inference API

def resolve_hf_resource(resource: str, as_model: bool = True) -> str:
    """Resolve a resource name to a full model identifier or deployment endpoint.
    Args:
        resource: Short name, repo ID, or deployment slug.
        as_model: If True, treat the resource as a model and query Hugging Face API.
    Returns:
        str: Fully qualified identifier or endpoint URL.
    Raises:
        ValueError: If the resource cannot be resolved.
    """
    api = HfApi()
    if as_model:
        # Try to find a model matching the name
        try:
            model_info = api.model_info(resource)
            return f"repo:{model_info.modelId}"
        except Exception:
            # If not found, assume it's a deployment URL
            return resource
    else:
        # Resolve a deployment endpoint directly via API
        deployments = api.list_deployments()
        for d in deployments:
            if d.modelId == resource:
                return d.apiUrl
        raise ValueError(f"Deployment '{resource}' not found on Hugging Face")
