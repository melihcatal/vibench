"""[SAME-SCENARIO] invoke_platform_model.py - invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client

Uses provided local client utilities from model_client.py and normalization helpers from model_models.py.
"""

import os
from model_client import get_managed_model_client
from model_models import PlatformInvocationResult


def invoke_model(
    deployment_id: str,
    input_text: str,
    **kwargs,
) -> PlatformInvocationResult:
    """Invoke the configured provider model and return a structured result.

    Args:
        deployment_id: Identifier for the deployment or model profile.
        input_text: Text prompt to send to the model.
        **kwargs: Additional provider-specific options.
    """
    client = get_managed_model_client()  # resolves credentials from env / config
    raw_response = client.invoke(
        deployment_id=deployment_id,
        prompt=input_text,
        **kwargs,
    )
    # Normalize response using helper
    result = (
        raw_response.to_dict() if hasattr(raw_response, "to_dict") else raw_response
    )
    return PlatformInvocationResult(
        data=result,
        provider="Amazon Bedrock",  # concrete provider identifier
    )
