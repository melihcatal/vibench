# [SAME-SCENARIO] select_platform_resource.py

# Resolve a provider-specific model identifier for invocation
# Example uses AWS Bedrock model ARN resolution (AWS credentials loaded from env)
import os
import boto3

AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
REGION = os.getenv("AWS_REGION", "us-east-1")

bedrock = boto3.client(
    "bedrock",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def resolve_bedrock_model(model_name: str) -> str:
    """Return the ARN for a Bedrock model by display name.

    Args:
        model_name: Human‑readable model name as shown in the Bedrock console.

    Returns:
        str: Full ARN of the model.
    """
    paginator = bedrock.get_paginator("list_models")
    for page in paginator.paginate():
        for model in page.get("models", []):
            if model["displayName"] == model_name:
                # Return the ARN, which Bedrock expects as ModelId
                return model["modelArn"]
    raise ValueError(
        f"Model '{model_name}' not found in Bedrock account '{AWS_ACCOUNT_ID}'"
    )
