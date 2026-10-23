# [SAME-SCENARIO] select_platform_resource.py
# Resolves a watsonx.ai model, deployment, or inference profile before invocation

import os
from typing import Optional, Dict


def resolve_resources(
    deployment_id: Optional[str] = None,
    model_id: Optional[str] = None,
    profile_id: Optional[str] = None,
    resource_path: Optional[str] = None,
) -> Dict[str, str]:
    """Select and validate a watsonx resource for model invocation.

    Args:
        deployment_id: Unique ID of a watsonx deployment.
        model_id: Unique ID of a watsonx model.
        profile_id: Optional inference profile ID for the project.
        resource_path: Path to a local resource (JSON/YAML) describing the resource.

    Returns:
        Dict containing the final selection (e.g., deployment_id) to be used by the invoker.
    """
    # Helper to prioritize inputs
    if deployment_id:
        return {"selected_deployment_id": deployment_id}
    if model_id:
        return {"selected_deployment_id": model_id}
    if profile_id:
        return {"selected_inference_profile_id": profile_id}
    if resource_path:
        # TODO: Load resource file and extract the relevant ID
        raise NotImplementedError("Resource path loading not implemented")
    raise ValueError("No valid watsonx resource provided")
