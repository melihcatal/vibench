# [LATER-STEP] record_text_safety.py

# Example using Amazon Bedrock Guardrails to check text safety
# Identifier: Service = Amazon Bedrock Guardrails, SDK = boto3

import boto3
from botocore.exceptions import ClientError


def is_text_safe(text: str) -> bool:
    """Check whether the supplied text complies with content safety policies.

    Uses Amazon Bedrock Guardrails (or Comprehend if preferred) to detect
    profanity, hateful content, or other unsafe language.

    Args:
        text (str): Untrusted user-generated content.

    Returns:
        bool: True if safe, False otherwise.
    """
    # Create a Bedrock client (AWS credentials via env vars)
    bedrock = boto3.client("bedrock-runtime")

    # Guardrails API call (example using the built‑in safety filter)
    try:
        response = bedrock.invoke_model(
            modelName="amazon.titan-text-light-v1",
            text=text,
            # Guardrails feature can be toggled via the request payload;
            # simplified here to just return a boolean.
        )
        # Assuming the response includes a "safe": true/false flag
        return response.get("safe", False)
    except ClientError as e:
        print(f"Safety check failed: {e}")
        return False  # safest default on failure
