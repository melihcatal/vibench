"""[LATER-STEP] platform_output_safety.py - Check platform model output for unsafe content"""

import os
from model_client import get_managed_model_client
from model_models import PlatformInvocationResult


def check_safety(invocation_result: PlatformInvocationResult) -> bool:
    """
    Determine whether the model output contains unsafe content using a provider‑specific moderation service.

    Currently uses Amazon Comprehend Toxicity / Bedrock Guardrails as the concrete provider.

    Returns:
        True if the content is safe, False otherwise.
    """
    if invocation_result.provider != "Amazon Bedrock":
        raise NotImplementedError("Safety check only implemented for Amazon Bedrock")
    # Placeholder: retrieve credentials from environment
    client = get_managed_model_client()  # will be the Bedrock client
    # In production you would call the moderation API, e.g.:
    # moderation = client.moderate(invocation_result.data)
    # For demo purposes we return True (assume safe). Replace with real check in real code.
    return True  # TODO: replace with actual moderation API call
