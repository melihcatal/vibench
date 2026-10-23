import os
from typing import Optional, Dict

MF_MODEL_ID = os.getenv("HF_MODEL_ID")


def resolve_model_or_deployment(
    project_id: Optional[str] = None,
    deployment_name: Optional[str] = None,
) -> str:
    """
    Resolve a Hugging Face model identifier (or deployment alias) using environment variables
    or optional arguments.  Raises ValueError if unable to determine a valid identifier.
    """
    # Prefer explicit arguments over env vars
    model_id = deployment_name or MF_MODEL_ID or project_id
    if not model_id:
        raise ValueError("No model identifier supplied. Set HF_MODEL_ID or pass deployment_name/project_id")
    # Simple validation: must be a non‑empty string
    if not isinstance(model_id, str) or not model_id.strip():
        raise ValueError("Model identifier must be a non‑empty string")
    # In a real scenario you might query the provider API for existence; here we
    # just return the resolved identifier.
    return model_id