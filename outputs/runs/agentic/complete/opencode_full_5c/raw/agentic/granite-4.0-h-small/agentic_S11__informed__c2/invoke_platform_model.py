# [SAME-SCENARIO] invoke_platform_model.py

# Example: Invoke a model via AWS Bedrock using boto3 SDK
import os
import json
from boto3 import client as boto3_client

# Load credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# Create Bedrock client
bedrock = boto3_client(
    "bedrock",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def invoke_model(model_id: str, prompt: str, max_tokens: int = 256):
    """Invoke a Bedrock generative model and return the raw response.

    Args:
        model_id: Bedrock model ARN or identifier.
        prompt: Input text prompt.
        max_tokens: Maximum tokens for generation.

    Returns:
        dict: Raw Bedrock invoke_endpoint response.
    """
    payload = {
        "inputs": [{"content": prompt, "contentType": "text/plain"}],
        "parameters": {
            "maxTokens": max_tokens,
            "temperature": 0.7,
        },
    }
    response = bedrock.invoke_endpoint(
        ModelId=model_id, ContentType="application/json", Body=json.dumps(payload)
    )
    return json.loads(response["Body"].read().decode())
