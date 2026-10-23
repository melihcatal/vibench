import os
from typing import Optional
from model_models import ModelResourceSpec

def select_platform_resource(
    deployment_name: Optional[str] = None,
    model_name: Optional[str] = None,
    inference_profile: Optional[str] = None,
) -> ModelResourceSpec:
    """
    Resolve the concrete platform resource (model + deployment/inference profile)
    based on configuration precedence:
    1. Explicit "deployment_name" (highest priority)
    2. Explicit "model_name" + optional "inference_profile"
    3. Default from environment variables if no arguments are supplied.
    Returns a ModelResourceSpec that the caller can pass to invocation helpers.
    """
    # Priority 1: explicit deployment name
    if deployment_name:
        return ModelResourceSpec(deployment=deployment_name)

    # Priority 2: model + optional profile
    if model_name:
        profile = inference_profile or os.getenv("DEFAULT_INFERENCE_PROFILE")
        return ModelResourceSpec(model=model_name, inference_profile=profile)

    # Priority 3: environment defaults (e.g., AWS Bedrock model ARN + alias)
    default_deployment = os.getenv("DEFAULT_DEPLOYMENT_ID")
    default_model = os.getenv("DEFAULT_MODEL_ID")
    default_profile = os.getenv("DEFAULT_INFERENCE_PROFILE")
    if default_deployment:
        return ModelResourceSpec(deployment=default_deployment)
    if default_model and default_profile:
        return ModelResourceSpec(model=default_model, inference_profile=default_profile)

    raise RuntimeError("No platform resource could be selected. Provide a deployment or model.")
